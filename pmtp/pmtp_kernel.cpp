// ============================================================================
// PMTP C++20 native shared-memory engine; platform runtime validation required
// Unifies C++, Rust, Dart and Python with strict byte-level parity.
// ============================================================================

#define BUILDING_PMTP_DLL
#include "pmtp_c_abi.h"
#include "pmtp_platform_shm.h"

#include <atomic>
#include <mutex>
#include <cstring>
#include <chrono>
#include <thread>
#include <new>
#include <random>
#include <cmath>

#define PMTP_FLAG_WRITER_BUSY 0x0001U

static inline size_t pmtp_dtype_get_itemsize(uint16_t dtype_id) {
    switch (dtype_id) {
        case PMTP_DTYPE_FP64:
        case PMTP_DTYPE_INT64:
        case PMTP_DTYPE_UINT64:
            return 8;
        case PMTP_DTYPE_FP32:
        case PMTP_DTYPE_INT32:
        case PMTP_DTYPE_UINT32:
            return 4;
        case PMTP_DTYPE_FP16:
        case PMTP_DTYPE_BF16:
        case PMTP_DTYPE_INT16:
        case PMTP_DTYPE_UINT16:
            return 2;
        case PMTP_DTYPE_INT8:
        case PMTP_DTYPE_UINT8:
            return 1;
        default:
            return 0; // Unsupported
    }
}

static inline bool pmtp_ranges_overlap(const void* p1, size_t len1, const void* p2, size_t len2) {
    if (!p1 || !p2 || len1 == 0 || len2 == 0) return false;
    const uintptr_t a = reinterpret_cast<uintptr_t>(p1);
    const uintptr_t b = reinterpret_cast<uintptr_t>(p2);
    if (a <= b) {
        return (b - a) < len1;
    } else {
        return (a - b) < len2;
    }
}

static inline bool pmtp_header_is_initialized(pmtp_header_compact_t* hdr) {
    if (!hdr) return false;
    std::atomic_ref<uint32_t> magic(hdr->magic);
    if (magic.load(std::memory_order_acquire) != PMTP_MAGIC_NUMBER || hdr->version != PMTP_VERSION_V1) return false;
    uint64_t epoch_nonce = 0;
    std::memcpy(&epoch_nonce, hdr->reserved_pad, sizeof(epoch_nonce));
    return epoch_nonce != 0;
}

struct pmtp_native_context_s {
    pmtp_shm_handle_t     shm_handle;
    uint32_t              slab_id;
    uint64_t              num_elements;
    uint16_t              dtype_id;
    size_t                itemsize;
    size_t                payload_bytes;
    int                   is_owner;
    std::mutex            local_mtx;
    std::atomic<uint64_t> local_leases[2]{};

    pmtp_header_compact_t* get_header() {
        return reinterpret_cast<pmtp_header_compact_t*>(shm_handle.pData);
    }

    void* get_slot_ptr(uint32_t slot) {
        if (!shm_handle.pData) return nullptr;
        uint8_t* base = reinterpret_cast<uint8_t*>(shm_handle.pData);
        size_t offset = sizeof(pmtp_header_compact_t) + (slot * payload_bytes);
        return base + offset;
    }
};

// Acquire one exact (slot, generation) pair, without reading retired_slot flags.
// Writer-owned retired flags are plain bytes and cannot be raced by readers.
// The writer lock and monotonically increasing generation are the synchronizers.
// This is a cooperative-process protocol, NOT an authorization mechanism.
static int pmtp_acquire_slot_coherent(
    pmtp_header_compact_t* hdr, uint32_t slot, uint64_t* out_generation
) {
    if (!hdr || slot > 1U || !out_generation) return -1;
    std::atomic_ref<uint16_t> writer_lock(hdr->reserved_flags);
    std::atomic_ref<uint32_t> active(hdr->active_slot);
    std::atomic_ref<uint32_t> gen(hdr->generation);
    std::atomic_ref<uint64_t> state(hdr->state_and_readers);
    if (!writer_lock.is_lock_free() || !active.is_lock_free() ||
        !gen.is_lock_free() || !state.is_lock_free()) return -7;
    const uint64_t increment = (slot == 0U) ? 1ULL : (1ULL << 32);
    for (unsigned attempt = 0; attempt < 10000U; ++attempt) {
        if (writer_lock.load(std::memory_order_acquire) & PMTP_FLAG_WRITER_BUSY)
            return -5;
        const uint32_t before_gen = gen.load(std::memory_order_acquire);
        if (before_gen == 0) return -10;
        if (active.load(std::memory_order_acquire) != slot) return -5;
        uint64_t cur = state.load(std::memory_order_acquire);
        if (cur & PMTP_DESTROYING_BIT) return -3;
        if (slot == 0U && (cur & PMTP_SLOT0_READERS_MASK) == PMTP_SLOT0_READERS_MASK) return -4;
        if (slot == 1U && ((cur & PMTP_SLOT1_READERS_MASK) >> 32) >= 0x7FFFFFFFULL) return -4;
        if (!state.compare_exchange_weak(cur, cur + increment,
                                         std::memory_order_acq_rel,
                                         std::memory_order_relaxed)) continue;
        const uint32_t after_gen = gen.load(std::memory_order_acquire);
        const uint32_t after_slot = active.load(std::memory_order_acquire);
        const uint16_t after_lock = writer_lock.load(std::memory_order_acquire);
        if (before_gen == after_gen && after_slot == slot &&
            !(after_lock & PMTP_FLAG_WRITER_BUSY)) {
            *out_generation = after_gen;
            return 0;
        }
        state.fetch_sub(increment, std::memory_order_release);
        return -5;
    }
    return -6;
}

extern "C" {

pmtp_native_context_t* pmtp_shm_create(
    const char* name, 
    uint32_t slab_id, 
    uint64_t num_elements, 
    uint16_t dtype_id
) {
    if (!name || num_elements == 0) return nullptr;

    size_t itemsize = pmtp_dtype_get_itemsize(dtype_id);
    if (itemsize == 0) return nullptr;

    if (num_elements > (SIZE_MAX - sizeof(pmtp_header_compact_t)) / (2 * itemsize)) return nullptr;
    size_t payload_bytes = static_cast<size_t>(num_elements) * itemsize;
    size_t total_bytes = sizeof(pmtp_header_compact_t) + (2 * payload_bytes);

    auto* ctx = new (std::nothrow) pmtp_native_context_s();
    if (!ctx) return nullptr;

    ctx->slab_id = slab_id;
    ctx->num_elements = num_elements;
    ctx->dtype_id = dtype_id;
    ctx->itemsize = itemsize;
    ctx->payload_bytes = payload_bytes;
    ctx->is_owner = 1;

    int rc = pmtp_platform_shm_create_or_open(name, total_bytes, 1, &ctx->shm_handle);
    if (rc != 0) {
        delete ctx;
        return nullptr;
    }

    ctx->is_owner = ctx->shm_handle.is_owner;
    pmtp_header_compact_t* hdr = ctx->get_header();
    if (ctx->is_owner) {
        // C14 Fix: Only zero-out and initialize header if we are the brand-new creator
        /* New POSIX/Windows shared mappings are zero-filled. Do not memset a named mapping
       after it becomes visible to other processes; publish magic atomically at the end. */
    hdr->version = PMTP_VERSION_V1;
    hdr->dtype_id = dtype_id;
    hdr->active_slot = 0;
    hdr->slab_id = slab_id;
    hdr->num_elements = num_elements;
    hdr->timestamp_ns = (uint64_t)std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::system_clock::now().time_since_epoch()).count();
    uint64_t epoch_nonce = hdr->timestamp_ns ^ static_cast<uint64_t>(reinterpret_cast<uintptr_t>(hdr));
    try {
        std::random_device rd;
        epoch_nonce ^= (static_cast<uint64_t>(rd()) << 32) ^ static_cast<uint64_t>(rd());
    } catch (...) { /* timestamp/address mix remains as a fallback nonce */ }
    if (epoch_nonce == 0) epoch_nonce = 1;
    std::memcpy(hdr->reserved_pad, &epoch_nonce, sizeof(epoch_nonce));
    hdr->scale = 1.0;
    hdr->generation = 0; // EMPTY state: 0 indicates unpublished
    hdr->retired_slot0 = 0;
    hdr->retired_slot1 = 1;
    hdr->state_and_readers = 0;
    std::atomic_ref<uint32_t> magic(hdr->magic);
    magic.store(PMTP_MAGIC_NUMBER, std::memory_order_release);
    }

    return ctx;
}

pmtp_native_context_t* pmtp_shm_open(
    const char* name, 
    uint32_t slab_id, 
    uint64_t num_elements, 
    uint16_t dtype_id
) {
    if (!name || num_elements == 0) return nullptr;

    size_t itemsize = pmtp_dtype_get_itemsize(dtype_id);
    if (itemsize == 0) return nullptr;

    if (num_elements > (SIZE_MAX - sizeof(pmtp_header_compact_t)) / (2 * itemsize)) return nullptr;
    size_t payload_bytes = static_cast<size_t>(num_elements) * itemsize;
    size_t total_bytes = sizeof(pmtp_header_compact_t) + (2 * payload_bytes);

    auto* ctx = new (std::nothrow) pmtp_native_context_s();
    if (!ctx) return nullptr;

    ctx->slab_id = slab_id;
    ctx->num_elements = num_elements;
    ctx->dtype_id = dtype_id;
    ctx->itemsize = itemsize;
    ctx->payload_bytes = payload_bytes;
    ctx->is_owner = 0; // Attached client, not owner

    int rc = pmtp_platform_shm_create_or_open(name, total_bytes, 0, &ctx->shm_handle);
    if (rc != 0) {
        delete ctx;
        return nullptr;
    }

    pmtp_header_compact_t* hdr = ctx->get_header();
    if (!pmtp_header_is_initialized(hdr)) {
        pmtp_platform_shm_close(&ctx->shm_handle);
        delete ctx;
        return nullptr;
    }
    uint64_t epoch_nonce = 0;
    std::memcpy(&epoch_nonce, hdr->reserved_pad, sizeof(epoch_nonce));
    // Bug #13/24 Fix: Validate slab_id match to prevent opening mismatched segments
    if (hdr->slab_id != slab_id || hdr->num_elements != num_elements || hdr->dtype_id != dtype_id || epoch_nonce == 0) {
        pmtp_platform_shm_close(&ctx->shm_handle);
        delete ctx;
        return nullptr;
    }

    return ctx;
}

int pmtp_shm_publish_atomic(
    pmtp_native_context_t* ctx, 
    const void* data, 
    uint64_t num_elements, 
    double scale
) {
    if (!ctx || !data || num_elements == 0) return -1;
    // A context-based attachment is a reader, never a publisher.
    // The raw pointer ABI has no authenticated owner identity and remains untrusted.
    if (!ctx->is_owner) return -12;
    if (!std::isfinite(scale)) return -9;
    if (num_elements != ctx->num_elements) return -2;

    std::lock_guard<std::mutex> lock(ctx->local_mtx);
    pmtp_header_compact_t* hdr = ctx->get_header();
    if (!hdr || !pmtp_header_is_initialized(hdr)) return -3;
    if (ctx->num_elements > (SIZE_MAX - sizeof(pmtp_header_compact_t)) / (2 * ctx->itemsize)) return -10;
    const size_t expected_mapping_bytes = sizeof(pmtp_header_compact_t) + 2 * static_cast<size_t>(ctx->num_elements) * ctx->itemsize;
    if (ctx->shm_handle.total_size < expected_mapping_bytes || hdr->num_elements != ctx->num_elements ||
        hdr->dtype_id != ctx->dtype_id) return -11;

    // std::atomic_ref is used only on naturally aligned fields in the shared mapping.
    std::atomic_ref<uint64_t> atomic_sr(hdr->state_and_readers);
    uint64_t current = atomic_sr.load(std::memory_order_acquire);
    if (current & PMTP_DESTROYING_BIT) {
        return -4; // Slab in destruction
    }

    // Inter-process writer synchronization spinlock using reserved_flags
    std::atomic_ref<uint16_t> atomic_flags(hdr->reserved_flags);
    uint16_t expected_flags = 0;
    bool writer_lock_acquired = false;
    for (uint32_t spin = 0; spin < 100000U; ++spin) {
        expected_flags = 0;
        if (atomic_flags.compare_exchange_weak(
                expected_flags, PMTP_FLAG_WRITER_BUSY,
                std::memory_order_acquire,
                std::memory_order_relaxed)) {
            writer_lock_acquired = true;
            break;
        }
        std::this_thread::yield();
    }
    if (!writer_lock_acquired) return -7; /* Busy/abandoned writer lock: fail closed. */
    current = atomic_sr.load(std::memory_order_acquire);
    if (current & PMTP_DESTROYING_BIT) {
        atomic_flags.store(0, std::memory_order_release);
        return -4;
    }

    std::atomic_ref<uint32_t> atomic_active(hdr->active_slot);
    uint32_t cur_active = atomic_active.load(std::memory_order_acquire);
    if (cur_active > 1U) {
        atomic_flags.store(0, std::memory_order_release);
        return -6;
    }
    uint32_t target_slot = 1U - cur_active;

    // Verify target slot has ZERO active readers
    current = atomic_sr.load(std::memory_order_acquire);
    uint64_t target_readers = (target_slot == 0) ? (current & PMTP_SLOT0_READERS_MASK) : ((current & PMTP_SLOT1_READERS_MASK) >> 32);
    if (target_readers > 0) {
        atomic_flags.store(0, std::memory_order_release);
        return -5; // Slot is currently leased by reader
    }

    void* dst = ctx->get_slot_ptr(target_slot);
    if (!dst) {
        atomic_flags.store(0, std::memory_order_release);
        return -6;
    }

    std::atomic_ref<uint32_t> atomic_gen(hdr->generation);
    if (atomic_gen.load(std::memory_order_acquire) == UINT32_MAX) {
        atomic_flags.store(0, std::memory_order_release);
        return -8; // Never wrap generation: recreate with a new epoch instead.
    }
    size_t copy_bytes = num_elements * ctx->itemsize;
    std::memmove(dst, data, copy_bytes);

    // Atomic update of metadata
    hdr->scale = scale;
    hdr->timestamp_ns = (uint64_t)std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::system_clock::now().time_since_epoch()).count();
    
    // Update retired flags BEFORE active_slot release store
    if (target_slot == 0) {
        hdr->retired_slot0 = 0;
        hdr->retired_slot1 = 1;
    } else {
        hdr->retired_slot0 = 1;
        hdr->retired_slot1 = 0;
    }

    // SOTA Linearization: Store active_slot with release semantics
    atomic_active.store(target_slot, std::memory_order_release);
    // Then advance generation atomically with release semantics
    atomic_gen.fetch_add(1, std::memory_order_release);

    // Release inter-process writer lock
    atomic_flags.store(0, std::memory_order_release);
    return 0; // Success
}

int pmtp_shm_publish_raw(void* buf_ptr, uint64_t mapping_bytes, const void* data, uint64_t num_elements, uint16_t dtype_id, double scale, uint32_t* out_generation) {
    if (!buf_ptr || !data || !out_generation || num_elements == 0 || ((uintptr_t)buf_ptr % 64) != 0) return -1;
    if (!std::isfinite(scale)) return -9;
    const size_t itemsize = pmtp_dtype_get_itemsize(dtype_id);
    if (itemsize == 0 || num_elements > (SIZE_MAX - sizeof(pmtp_header_compact_t)) / (2 * itemsize)) return -2;
    // Validate lengths before overlap checks; no overflowed unsigned products.
    if (pmtp_ranges_overlap(buf_ptr, mapping_bytes, out_generation, sizeof(uint32_t))) return -8;
    if (pmtp_ranges_overlap(buf_ptr, sizeof(pmtp_header_compact_t),
                            data, static_cast<size_t>(num_elements) * itemsize)) return -8;
    const size_t expected_mapping_bytes = sizeof(pmtp_header_compact_t) + 2 * static_cast<size_t>(num_elements) * itemsize;
    if (mapping_bytes < expected_mapping_bytes) return -11;
    auto* hdr = reinterpret_cast<pmtp_header_compact_t*>(buf_ptr);
    if (!pmtp_header_is_initialized(hdr) ||
        hdr->dtype_id != dtype_id || hdr->num_elements != num_elements) return -3;

    std::atomic_ref<uint16_t> writer_lock(hdr->reserved_flags);
    std::atomic_ref<uint64_t> state(hdr->state_and_readers);
    std::atomic_ref<uint32_t> active(hdr->active_slot);
    std::atomic_ref<uint32_t> generation(hdr->generation);
    if (!writer_lock.is_lock_free() || !state.is_lock_free() || !active.is_lock_free() || !generation.is_lock_free()) return -7;

    uint16_t expected = 0;
    bool acquired = false;
    /* Bounded wait: a crashed writer must not hang this caller forever. */
    for (uint32_t spin = 0; spin < 100000U; ++spin) {
        expected = 0;
        if (writer_lock.compare_exchange_weak(expected, PMTP_FLAG_WRITER_BUSY,
                std::memory_order_acquire, std::memory_order_relaxed)) {
            acquired = true;
            break;
        }
        if (state.load(std::memory_order_acquire) & PMTP_DESTROYING_BIT) return -4;
        std::this_thread::yield();
    }
    if (!acquired) return -6; /* Busy or abandoned lock: fail closed, never spin forever. */
    auto unlock = [&]() { writer_lock.store(0, std::memory_order_release); };
    if (state.load(std::memory_order_acquire) & PMTP_DESTROYING_BIT) { unlock(); return -4; }

    const uint32_t current_slot = active.load(std::memory_order_acquire);
    if (current_slot > 1U) { unlock(); return -3; }
    const uint32_t target_slot = 1U - current_slot;
    const uint64_t readers = state.load(std::memory_order_acquire);
    const uint64_t target_readers = target_slot == 0
        ? (readers & PMTP_SLOT0_READERS_MASK)
        : ((readers & PMTP_SLOT1_READERS_MASK) >> 32);
    if (target_readers != 0) { unlock(); return -5; }

    if (generation.load(std::memory_order_acquire) == UINT32_MAX) { unlock(); return -8; }
    const size_t payload_bytes = static_cast<size_t>(num_elements) * itemsize;
    auto* base = static_cast<uint8_t*>(buf_ptr);
    void* dst = base + sizeof(pmtp_header_compact_t) + static_cast<size_t>(target_slot) * payload_bytes;
    std::memmove(dst, data, payload_bytes);
    hdr->scale = scale;
    hdr->timestamp_ns = static_cast<uint64_t>(std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::system_clock::now().time_since_epoch()).count());
    hdr->retired_slot0 = static_cast<uint8_t>(target_slot != 0);
    hdr->retired_slot1 = static_cast<uint8_t>(target_slot != 1);
    // SOTA Linearization: Switch active slot first
    active.store(target_slot, std::memory_order_release);
    // Then advance generation atomically
    const uint32_t next_gen = generation.fetch_add(1, std::memory_order_release) + 1U;
    *out_generation = next_gen;
    unlock();
    return 0;
}

int pmtp_shm_commit_header_raw(void* buf_ptr) {
    if (!buf_ptr || ((uintptr_t)buf_ptr % 64) != 0) return -1;
    auto* hdr = reinterpret_cast<pmtp_header_compact_t*>(buf_ptr);
    std::atomic_ref<uint32_t> magic(hdr->magic);
    if (magic.load(std::memory_order_acquire) != 0) return -2; // only a fresh slab can be committed
    if (hdr->version != PMTP_VERSION_V1 || hdr->active_slot > 1 || hdr->num_elements == 0 ||
        pmtp_dtype_get_itemsize(hdr->dtype_id) == 0) return -3;
    uint64_t epoch_nonce = 0;
    std::memcpy(&epoch_nonce, hdr->reserved_pad, sizeof(epoch_nonce));
    if (epoch_nonce == 0 || hdr->state_and_readers != 0 || hdr->reserved_flags != 0) return -4;
    magic.store(PMTP_MAGIC_NUMBER, std::memory_order_release);
    return 0;
}

int pmtp_shm_mark_destroying_raw(void* buf_ptr) {
    if (!buf_ptr || ((uintptr_t)buf_ptr % 64) != 0) return -1;
    auto* hdr = reinterpret_cast<pmtp_header_compact_t*>(buf_ptr);
    if (!pmtp_header_is_initialized(hdr)) return -2;
    std::atomic_ref<uint16_t> writer_lock(hdr->reserved_flags);
    std::atomic_ref<uint64_t> state(hdr->state_and_readers);
    if (!writer_lock.is_lock_free() || !state.is_lock_free()) return -7;
    bool acquired = false;
    uint16_t expected = 0;
    for (uint32_t spin = 0; spin < 100000U; ++spin) {
        expected = 0;
        if (writer_lock.compare_exchange_weak(expected, PMTP_FLAG_WRITER_BUSY,
                std::memory_order_acquire, std::memory_order_relaxed)) {
            acquired = true;
            break;
        }
        std::this_thread::yield();
    }
    if (!acquired) return -6;
    state.fetch_or(PMTP_DESTROYING_BIT, std::memory_order_acq_rel);
    writer_lock.store(0, std::memory_order_release);
    return 0;
}

int pmtp_shm_read_header_raw(void* buf_ptr, void* out_header_64b) {
    if (!buf_ptr || !out_header_64b || ((uintptr_t)buf_ptr % 64) != 0) return -1;
    // RT-043 Fix: Check for buffer aliasing/overlap between source and destination
    if (pmtp_ranges_overlap(buf_ptr, sizeof(pmtp_header_compact_t),
                            out_header_64b, sizeof(pmtp_header_compact_t))) return -8;
    auto* hdr = reinterpret_cast<pmtp_header_compact_t*>(buf_ptr);
    if (!pmtp_header_is_initialized(hdr)) return -2;
    auto* out = static_cast<uint8_t*>(out_header_64b);
    std::atomic_ref<uint16_t> writer_lock(hdr->reserved_flags);
    std::atomic_ref<uint64_t> state(hdr->state_and_readers);
    if (!writer_lock.is_lock_free() || !state.is_lock_free()) return -7;

    bool acquired = false;
    uint16_t expected = 0;
    for (uint32_t spin = 0; spin < 100000U; ++spin) {
        expected = 0;
        if (writer_lock.compare_exchange_weak(expected, PMTP_FLAG_WRITER_BUSY,
                std::memory_order_acquire, std::memory_order_relaxed)) {
            acquired = true;
            break;
        }
        std::this_thread::yield();
    }
    if (!acquired) return -6;

    /* Writer-owned fields are stable under this lock. Reader counters remain atomic. */
    std::memcpy(out, buf_ptr, offsetof(pmtp_header_compact_t, reserved_flags));
    const uint16_t flags_snapshot = 0;
    std::memcpy(out + offsetof(pmtp_header_compact_t, reserved_flags), &flags_snapshot, sizeof(flags_snapshot));
    const uint64_t state_snapshot = state.load(std::memory_order_acquire);
    std::memcpy(out + offsetof(pmtp_header_compact_t, state_and_readers), &state_snapshot, sizeof(state_snapshot));
    std::memcpy(out + offsetof(pmtp_header_compact_t, reserved_pad), hdr->reserved_pad, sizeof(hdr->reserved_pad));
    writer_lock.store(0, std::memory_order_release);
    return 0;
}

int pmtp_shm_acquire_lease(
    pmtp_native_context_t* ctx,
    uint32_t slot,
    uint64_t* out_generation
) {
    if (!ctx || slot > 1U || !out_generation) return -1;
    const size_t total_bytes = sizeof(pmtp_header_compact_t) + 2 * ctx->payload_bytes;
    if (pmtp_ranges_overlap(ctx->shm_handle.pData, total_bytes,
                            out_generation, sizeof(uint64_t))) return -8;
    std::lock_guard<std::mutex> guard(ctx->local_mtx);
    auto* hdr = ctx->get_header();
    if (!hdr || !pmtp_header_is_initialized(hdr)) return -2;
    const int rc = pmtp_acquire_slot_coherent(hdr, slot, out_generation);
    if (rc == 0) ctx->local_leases[slot].fetch_add(1, std::memory_order_relaxed);
    return rc;
}

int pmtp_shm_release_lease(pmtp_native_context_t* ctx, uint32_t slot) {
    if (!ctx || slot > 1) return -1;
    std::lock_guard<std::mutex> local_lock(ctx->local_mtx);
    if (ctx->local_leases[slot].load(std::memory_order_relaxed) == 0) return -4;

    pmtp_header_compact_t* hdr = ctx->get_header();
    if (!hdr) return -2;

    std::atomic_ref<uint64_t> atomic_sr(hdr->state_and_readers);
    uint64_t decrement = (slot == 0) ? 1ULL : (1ULL << 32);

    uint64_t current = atomic_sr.load(std::memory_order_relaxed);
    while (true) {
        uint64_t slot_readers = (slot == 0) ? (current & PMTP_SLOT0_READERS_MASK) : ((current & PMTP_SLOT1_READERS_MASK) >> 32);
        if (slot_readers == 0) {
            return -3; // Double-release guard
        }

        if (atomic_sr.compare_exchange_weak(
                current,
                current - decrement,
                std::memory_order_release,
                std::memory_order_relaxed)) {
            break;
        }
    }

    ctx->local_leases[slot].fetch_sub(1, std::memory_order_relaxed);
    return 0; // Released
}

int pmtp_shm_acquire_lease_raw(void* buf_ptr, uint32_t slot, uint64_t* out_generation) {
    if (!buf_ptr || (reinterpret_cast<uintptr_t>(buf_ptr) & 63U) ||
        slot > 1U || !out_generation) return -1;
    if (pmtp_ranges_overlap(buf_ptr, sizeof(pmtp_header_compact_t),
                            out_generation, sizeof(uint64_t))) return -8;
    auto* hdr = static_cast<pmtp_header_compact_t*>(buf_ptr);
    if (!pmtp_header_is_initialized(hdr)) return -2;
    return pmtp_acquire_slot_coherent(hdr, slot, out_generation);
}

int pmtp_shm_acquire_consistent_raw(
    void* buf_ptr,
    uint32_t* out_slot,
    uint64_t* out_generation
) {
    if (!buf_ptr || !out_slot || !out_generation ||
        (reinterpret_cast<uintptr_t>(buf_ptr) & 63U)) return -1;
    if (pmtp_ranges_overlap(buf_ptr, sizeof(pmtp_header_compact_t), out_slot, sizeof(uint32_t)) ||
        pmtp_ranges_overlap(buf_ptr, sizeof(pmtp_header_compact_t), out_generation, sizeof(uint64_t)) ||
        pmtp_ranges_overlap(out_slot, sizeof(uint32_t), out_generation, sizeof(uint64_t))) return -8;
    auto* hdr = static_cast<pmtp_header_compact_t*>(buf_ptr);
    if (!pmtp_header_is_initialized(hdr)) return -2;
    std::atomic_ref<uint32_t> active(hdr->active_slot);
    for (unsigned attempt = 0; attempt < 10000U; ++attempt) {
        const uint32_t slot = active.load(std::memory_order_acquire);
        if (slot > 1U) return -5;
        uint64_t acquired_generation = 0;
        const int rc = pmtp_acquire_slot_coherent(hdr, slot, &acquired_generation);
        if (rc == 0) {
            *out_slot = slot;
            *out_generation = acquired_generation;
            return 0;
        }
        if (rc != -5 && rc != -6) return rc;
        std::this_thread::yield();
    }
    return -6;
}

int pmtp_shm_release_lease_raw(void* buf_ptr, uint32_t slot) {
    if (!buf_ptr || ((uintptr_t)buf_ptr % 64) != 0 || slot > 1) return -1;
    pmtp_header_compact_t* hdr = reinterpret_cast<pmtp_header_compact_t*>(buf_ptr);
    if (!pmtp_header_is_initialized(hdr)) return -4;
    std::atomic_ref<uint64_t> atomic_sr(hdr->state_and_readers);
    uint64_t decrement = (slot == 0) ? 1ULL : (1ULL << 32);

    uint64_t current = atomic_sr.load(std::memory_order_relaxed);
    while (true) {
        uint64_t slot_readers = (slot == 0) ? (current & PMTP_SLOT0_READERS_MASK) : ((current & PMTP_SLOT1_READERS_MASK) >> 32);
        if (slot_readers == 0) {
            return -3; // Double-release guard
        }

        if (atomic_sr.compare_exchange_weak(
                current,
                current - decrement,
                std::memory_order_release,
                std::memory_order_relaxed)) {
            break;
        }
    }
    return 0; // Released
}

int pmtp_shm_read_leased(
    pmtp_native_context_t* ctx, 
    void* out_buffer, 
    uint64_t buffer_capacity_bytes,
    uint32_t* out_slot, 
    uint64_t* out_generation
) {
    if (!ctx || !out_buffer || buffer_capacity_bytes < ctx->payload_bytes) return -1;
    // RT-045: Precondition validation: reject out_buffer, out_slot, or out_generation overlapping with mapping
    const size_t total_mapping_bytes = sizeof(pmtp_header_compact_t) + 2 * ctx->payload_bytes;
    if (pmtp_ranges_overlap(ctx->shm_handle.pData, total_mapping_bytes, out_buffer, ctx->payload_bytes)) return -8;
    if (out_slot && pmtp_ranges_overlap(ctx->shm_handle.pData, total_mapping_bytes, out_slot, sizeof(uint32_t))) return -8;
    if (out_generation && pmtp_ranges_overlap(ctx->shm_handle.pData, total_mapping_bytes, out_generation, sizeof(uint64_t))) return -8;
    if (out_slot && pmtp_ranges_overlap(out_buffer, ctx->payload_bytes, out_slot, sizeof(uint32_t))) return -8;
    if (out_generation && pmtp_ranges_overlap(out_buffer, ctx->payload_bytes, out_generation, sizeof(uint64_t))) return -8;
    if (out_slot && out_generation &&
        pmtp_ranges_overlap(out_slot, sizeof(uint32_t), out_generation, sizeof(uint64_t))) return -8;

    pmtp_header_compact_t* hdr = ctx->get_header();
    if (!hdr) return -2;

    std::atomic_ref<uint32_t> atomic_active(hdr->active_slot);
    uint32_t active_slot = atomic_active.load(std::memory_order_acquire);
    uint64_t gen = 0;

    int rc = pmtp_shm_acquire_lease(ctx, active_slot, &gen);
    if (rc != 0) return rc;

    void* src = ctx->get_slot_ptr(active_slot);
    if (!src) {
        pmtp_shm_release_lease(ctx, active_slot);
        return -3;
    }

    std::memcpy(out_buffer, src, ctx->payload_bytes);
    pmtp_shm_release_lease(ctx, active_slot);

    if (out_slot) *out_slot = active_slot;
    if (out_generation) *out_generation = gen;
    return 0;
}

const void* pmtp_shm_get_leased_ptr(pmtp_native_context_t* ctx, uint32_t slot) {
    if (!ctx || slot > 1) return nullptr;
    // Global reader count is NOT proof this context holds a lease.
    if (ctx->local_leases[slot].load(std::memory_order_acquire) == 0) return nullptr;
    pmtp_header_compact_t* hdr = ctx->get_header();
    if (!hdr) return nullptr;
    std::atomic_ref<uint64_t> state(hdr->state_and_readers);
    const uint64_t current = state.load(std::memory_order_acquire);
    const uint64_t readers = slot == 0 ? (current & PMTP_SLOT0_READERS_MASK)
                                      : ((current & PMTP_SLOT1_READERS_MASK) >> 32);
    if (readers == 0 || (current & PMTP_DESTROYING_BIT)) return nullptr;
    return ctx->get_slot_ptr(slot); /* Caller must retain its own lease until done. */
}

int pmtp_shm_close_checked(pmtp_native_context_t* ctx, uint32_t timeout_ms) {
    if (!ctx) return -1;
    /* Caller must externally serialize close against all other calls using this ctx. */
    std::unique_lock<std::mutex> local_lock(ctx->local_mtx);
    pmtp_header_compact_t* hdr = ctx->get_header();
    if (!hdr) return -2;
    /* Refuse before marking DESTROYING if this context itself still owns a lease. */
    if (ctx->local_leases[0].load(std::memory_order_acquire) != 0 ||
        ctx->local_leases[1].load(std::memory_order_acquire) != 0) return -5;
    if (ctx->is_owner) {
        const int mark_rc = pmtp_shm_mark_destroying_raw(hdr);
        if (mark_rc != 0) return -3;
        std::atomic_ref<uint64_t> state(hdr->state_and_readers);
        const auto deadline = std::chrono::steady_clock::now() + std::chrono::milliseconds(timeout_ms);
        for (;;) {
            const uint64_t readers = state.load(std::memory_order_acquire) & PMTP_READERS_MASK;
            if (readers == 0) break;
            if (timeout_ms == 0 || std::chrono::steady_clock::now() >= deadline) return -4;
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        }
    }
    local_lock.unlock();
    pmtp_platform_shm_close(&ctx->shm_handle);
    delete ctx;
    return 0;
}

void pmtp_shm_close(pmtp_native_context_t* ctx) {
    /* Compatibility API. E-008/CR-2: Extended drain timeout to 2000 ms to honor contract. */
    int rc = pmtp_shm_close_checked(ctx, 2000);
    if (rc != 0) {
        std::fprintf(stderr, "[pmtp_shm_close] Warning: close_checked returned %d (drain timeout or error)\n", rc);
    }
}

} // extern "C"
