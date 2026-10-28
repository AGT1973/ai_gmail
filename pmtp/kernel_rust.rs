// =============================================================================
// PMTP Rust kernel and compact-header definitions; native build/runtime validation required
// Unifies C++, Rust, Dart and Python with strict byte-level parity.
// =============================================================================

use std::sync::atomic::{AtomicU16, AtomicU32, AtomicU64, Ordering};

pub const PMTP_MAGIC: u32 = 0x504D5450; // "PMTP"
pub const PMTP_VERSION: u16 = 0x0001;

pub const PMTP_DESTROYING_BIT: u64 = 1u64 << 63;
pub const PMTP_READERS_MASK: u64 = !PMTP_DESTROYING_BIT;
pub const PMTP_SLOT0_READERS_MASK: u64 = 0x00000000FFFFFFFF;
pub const PMTP_SLOT1_READERS_MASK: u64 = 0x7FFFFFFF00000000;

// =============================================================================
// 1. CABECERA COMPACTA ALINEADA A CACHE LINE (64 BYTES EXACTOS)
// =============================================================================
#[repr(C, align(64))]
pub struct PmtpHeaderCompact {
    pub magic: u32,                  // Offset  0 (4B): 0x504D5450
    pub version: u16,                // Offset  4 (2B): 1
    pub dtype_id: u16,               // Offset  6 (2B): 1 (FP64 default)
    pub active_slot: AtomicU32,      // Offset  8 (4B): must be atomic against native C++ writers
    pub slab_id: u32,                // Offset 12 (4B): Identificador de slab
    pub num_elements: u64,           // Offset 16 (8B): Escalares por slot
    pub timestamp_ns: u64,           // Offset 24 (8B): Timestamp POSIX nanosegundos
    pub scale: f64,                  // Offset 32 (8B): Escala IEEE-754
    pub generation: AtomicU32,       // Offset 40 (4B): monotonic counter, never read non-atomically
    pub retired_slot0: u8,           // Offset 44 (1B): Retiro slot 0
    pub retired_slot1: u8,           // Offset 45 (1B): Retiro slot 1
    pub reserved_flags: AtomicU16,   // Offset 46 (2B): shared writer lock
    // Offset 48 (8B): Bit 63 = DESTROYING, Bits 32-62 = slot1, Bits 0-31 = slot0
    pub state_and_readers: AtomicU64,
    pub reserved_pad: [u8; 8],       // Offset 56 (8B) -> Total 64 bytes exactos
}

impl PmtpHeaderCompact {
    pub fn new(slab_id: u32, num_elements: u64) -> Self {
        let timestamp_ns = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default().as_nanos() as u64;
        let mut epoch = timestamp_ns ^ (u64::from(slab_id).rotate_left(17)) ^ num_elements.rotate_left(31);
        if epoch == 0 { epoch = 1; }
        Self {
            magic: PMTP_MAGIC,
            version: PMTP_VERSION,
            dtype_id: 1, // FP64
            active_slot: AtomicU32::new(0),
            slab_id,
            num_elements,
            timestamp_ns,
            scale: 1.0,
            generation: AtomicU32::new(1),
            retired_slot0: 0,
            retired_slot1: 1,
            reserved_flags: AtomicU16::new(0),
            state_and_readers: AtomicU64::new(0),
            reserved_pad: epoch.to_le_bytes(),
        }
    }

    /// Adquiere lease atómico sobre el slot correspondiente libre de carreras
    pub fn acquire_reader_lease(&self, slot: u32) -> Result<u64, &'static str> {
        if slot > 1 {
            return Err("INVALID_SLOT");
        }
        if slot != self.active_slot.load(Ordering::Acquire) {
            return Err("SLOT_INACTIVE");
        }
        let increment: u64 = if slot == 0 { 1u64 } else { 1u64 << 32 };
        let mut current = self.state_and_readers.load(Ordering::Relaxed);

        loop {
            if (current & PMTP_DESTROYING_BIT) != 0 {
                return Err("SLAB_IN_DESTRUCTION");
            }

            // Validar que el contador de lectores del slot no desborde hacia el otro slot
            if slot == 0 && (current & PMTP_SLOT0_READERS_MASK) == PMTP_SLOT0_READERS_MASK {
                return Err("SLOT0_READERS_OVERFLOW");
            }
            if slot == 1 && ((current & PMTP_SLOT1_READERS_MASK) >> 32) >= 0x7FFFFFFF {
                return Err("SLOT1_READERS_OVERFLOW");
            }

            match self.state_and_readers.compare_exchange_weak(
                current,
                current + increment,
                Ordering::Acquire,
                Ordering::Relaxed,
            ) {
                Ok(_) => {
                    if slot != self.active_slot.load(Ordering::Acquire) {
                        self.state_and_readers.fetch_sub(increment, Ordering::Release);
                        return Err("SLOT_SWITCHED_DURING_ACQUISITION");
                    }
                    return Ok(self.generation.load(Ordering::Acquire) as u64);
                },
                Err(actual) => current = actual,
            }
        }
    }

    /// Libera lease de lectura decrementando los lectores del slot correspondiente
    pub fn release_reader_lease(&self, slot: u32) -> Result<(), &'static str> {
        if slot > 1 {
            return Err("INVALID_SLOT");
        }
        let decrement: u64 = if slot == 0 { 1u64 } else { 1u64 << 32 };
        let mut current = self.state_and_readers.load(Ordering::Relaxed);

        loop {
            let slot_readers = if slot == 0 {
                current & PMTP_SLOT0_READERS_MASK
            } else {
                (current & PMTP_SLOT1_READERS_MASK) >> 32
            };

            if slot_readers == 0 {
                return Err("DOUBLE_RELEASE_OR_ZERO_READERS");
            }

            match self.state_and_readers.compare_exchange_weak(
                current,
                current - decrement,
                Ordering::Release,
                Ordering::Relaxed,
            ) {
                Ok(_) => return Ok(()),
                Err(actual) => current = actual,
            }
        }
    }

    /// Atomically blocks new writers/readers, then drains readers. Returns false on timeout.
    pub fn mark_destroying_and_drain(&self, timeout_ms: u64) -> bool {
        let start = std::time::Instant::now();
        let timeout = std::time::Duration::from_millis(timeout_ms);
        let mut acquired = false;
        while start.elapsed() < timeout {
            if self.reserved_flags.compare_exchange_weak(
                0, 1, Ordering::Acquire, Ordering::Relaxed
            ).is_ok() {
                acquired = true;
                break;
            }
            std::hint::spin_loop();
        }
        if !acquired { return false; }
        self.state_and_readers.fetch_or(PMTP_DESTROYING_BIT, Ordering::AcqRel);
        self.reserved_flags.store(0, Ordering::Release);

        while (self.state_and_readers.load(Ordering::Acquire) & PMTP_READERS_MASK) != 0 {
            if start.elapsed() >= timeout { return false; }
            std::hint::spin_loop();
        }
        true
    }

}

// =============================================================================
// 2. CABECERA WIRE DE 128 BYTES (PARIDAD ESTRICTA C-DART-RUST CON ALINEACIÓN NATURAL 8B)
// =============================================================================
#[repr(C)]
pub struct PolydimWireHeader {
    pub magic: u32,                  // Offset  0 (4B): 0x504D5450
    pub version_major: u16,          // Offset  4 (2B): 1
    pub version_minor: u16,          // Offset  6 (2B): 0
    pub slab_uuid: [u8; 16],         // Offset  8 (16B): UUID
    pub num_elements: u64,           // Offset 24 (8B): Cantidad de elementos
    pub payload_bytes: u64,          // Offset 32 (8B): Tamaño en bytes
    pub timestamp_ns: u64,           // Offset 40 (8B): Timestamp nanosegundos
    pub dtype: u32,                  // Offset 48 (4B): DType
    pub _pad_dtype: u32,             // Offset 52 (4B): Relleno explícito alineación a 64 bits
    pub stiefel_defect: f64,         // Offset 56 (8B): Defecto ortonormal (Alineado a 8B)
    pub blake2s_hash: [u8; 32],      // Offset 64 (32B): Hash
    pub reserved: [u8; 32],          // Offset 96 (32B) -> Total 128 bytes
}

// Aserciones estáticas de paridad binaria
const _: () = {
    assert!(std::mem::size_of::<PmtpHeaderCompact>() == 64);
    assert!(std::mem::size_of::<PolydimWireHeader>() == 128);
};

// =============================================================================
// 3. ACUMULADOR COMPENSADO DE NEUMAIER (PRECISIÓN FP64 <= 1e-15)
// =============================================================================
#[repr(C)]
pub struct NeumaierAccumulator {
    sum: f64,
    compensation: f64,
}

impl NeumaierAccumulator {
    pub fn new() -> Self {
        Self { sum: 0.0, compensation: 0.0 }
    }

    pub fn add(&mut self, value: f64) {
        let t = self.sum + value;
        if self.sum.abs() >= value.abs() {
            self.compensation += (self.sum - t) + value;
        } else {
            self.compensation += (value - t) + self.sum;
        }
        self.sum = t;
    }

    pub fn total(&self) -> f64 {
        self.sum + self.compensation
    }
}

pub fn neumaier_norm(data: &[f64]) -> f64 {
    if data.is_empty() {
        return 0.0;
    }
    // Bug #8 Fix: LAPACK Blue's scaling to prevent underflow/overflow on extreme exponents
    let mut max_val = 0.0f64;
    for &x in data {
        let ax = x.abs();
        if ax > max_val {
            max_val = ax;
        }
    }
    if max_val == 0.0 || !max_val.is_finite() {
        return max_val;
    }
    let inv_max = 1.0 / max_val;
    let mut acc = NeumaierAccumulator::new();
    for &x in data {
        let scaled = x * inv_max;
        acc.add(scaled * scaled);
    }
    max_val * acc.total().sqrt()
}

// =============================================================================
// 4. RETRACCIÓN NEWTON-SCHULZ REAL DE ORDEN 5 (CÁLCULO MATRICIAL RIGUROSO)
// W_{k+1} = 1/8 * W_k * (15 I - 10 M + 3 M^2), donde M = W_k^T W_k
// =============================================================================
pub fn newton_schulz_ord5_retract(
    w: &mut [f64], rows: usize, cols: usize, max_iters: usize, tol: f64
) -> Result<f64, &'static str> {
    let expected_len = rows.checked_mul(cols).ok_or("DIMENSION_OVERFLOW")?;
    if rows < cols || cols == 0 || w.len() != expected_len {
        return Err("DIMENSION_MISMATCH");
    }
    if !tol.is_finite() || tol <= 0.0 {
        return Err("INVALID_TOLERANCE");
    }
    let mut working = w.to_vec();
    let defect = newton_schulz_ord5_retract_in_place(&mut working, rows, cols, max_iters, tol)?;
    w.copy_from_slice(&working);
    Ok(defect)
}

fn newton_schulz_ord5_retract_in_place(
    w: &mut [f64], rows: usize, cols: usize, max_iters: usize, tol: f64
) -> Result<f64, &'static str> {
    if rows.checked_mul(cols) != Some(w.len()) || rows < cols || cols == 0 {
        return Err("DIMENSION_MISMATCH");
    }
    let square_len = cols.checked_mul(cols).ok_or("DIMENSION_OVERFLOW")?;

    // 1. Preescalado espectral estricto: W0 = W / ||W||_F (garantiza ||W0||_2 <= 1)
    let mut norm_acc = NeumaierAccumulator::new();
    for &x in w.iter() {
        norm_acc.add(x * x);
    }
    let frob_norm = norm_acc.total().sqrt();
    if frob_norm <= 0.0 || !frob_norm.is_finite() {
        return Err("SINGULAR_OR_NONFINITE_MATRIX");
    }

    // Escalamos para que el mayor valor singular esté en radio de convergencia (0, sqrt(3))
    // Normalización por norma de Frobenius; la convergencia aún depende del rango y del número de iteraciones.
    let scale_factor = 1.0 / frob_norm;
    for x in w.iter_mut() {
        *x *= scale_factor;
    }

    let mut m = vec![0.0f64; square_len];
    let mut m2 = vec![0.0f64; square_len];
    let mut poly = vec![0.0f64; square_len];
    let mut w_next = vec![0.0f64; w.len()];

    let mut final_defect = 1.0f64;

    for _ in 0..max_iters {
        // a) Producto Gram con suma compensada para reducir error de acumulación.
        m.fill(0.0);
        for i in 0..cols {
            for j in 0..cols {
                let mut dot = NeumaierAccumulator::new();
                for r in 0..rows {
                    dot.add(w[r * cols + i] * w[r * cols + j]);
                }
                m[i * cols + j] = dot.total();
            }
        }

        // Medir defecto de ortogonalidad ||M - I||_frobenius
        let mut def_acc = NeumaierAccumulator::new();
        for i in 0..cols {
            for j in 0..cols {
                let expected = if i == j { 1.0 } else { 0.0 };
                let diff = m[i * cols + j] - expected;
                def_acc.add(diff * diff);
            }
        }
        final_defect = def_acc.total().sqrt();
        if final_defect < tol {
            return Ok(final_defect);
        }

        // b) Calcular M^2 = M * M (cols x cols)
        for i in 0..cols {
            for j in 0..cols {
                let mut dot = NeumaierAccumulator::new();
                for k in 0..cols {
                    dot.add(m[i * cols + k] * m[k * cols + j]);
                }
                m2[i * cols + j] = dot.total();
            }
        }

        // c) Polinomio de Orden 5: Poly = (15 I - 10 M + 3 M^2) / 8
        for i in 0..cols {
            for j in 0..cols {
                let id = if i == j { 15.0 } else { 0.0 };
                poly[i * cols + j] = (id - 10.0 * m[i * cols + j] + 3.0 * m2[i * cols + j]) / 8.0;
            }
        }

        // d) W_next = W * Poly (rows x cols)
        for r in 0..rows {
            for c in 0..cols {
                let mut dot = NeumaierAccumulator::new();
                for k in 0..cols {
                    dot.add(w[r * cols + k] * poly[k * cols + c]);
                }
                w_next[r * cols + c] = dot.total();
            }
        }

        w.copy_from_slice(&w_next);

        // e) Recalculo estricto de defecto sobre la matriz W recien actualizada
        m.fill(0.0);
        for i in 0..cols {
            for j in 0..cols {
                let mut dot = NeumaierAccumulator::new();
                for r in 0..rows {
                    dot.add(w[r * cols + i] * w[r * cols + j]);
                }
                m[i * cols + j] = dot.total();
            }
        }
        let mut def_acc = NeumaierAccumulator::new();
        for i in 0..cols {
            for j in 0..cols {
                let expected = if i == j { 1.0 } else { 0.0 };
                let diff = m[i * cols + j] - expected;
                def_acc.add(diff * diff);
            }
        }
        final_defect = def_acc.total().sqrt();
        if final_defect < tol {
            return Ok(final_defect);
        }
    }

    if final_defect < tol {
        Ok(final_defect)
    } else {
        Err("CONVERGENCE_NOT_REACHED")
    }
}

// =============================================================================
// 5. C-ABI EXPORTS PARA CARGA DIRECTA DESDE PYTHON/DART FFI
// =============================================================================
#[no_mangle]
pub unsafe extern "C" fn rust_newton_schulz_ord5_retract(
    w_ptr: *mut f64,
    len: usize,
    rows: usize,
    cols: usize,
    max_iters: usize,
    tol: f64,
    out_defect: *mut f64
) -> i32 {
    if w_ptr.is_null() || out_defect.is_null() || rows.checked_mul(cols) != Some(len) ||
        cols == 0 || rows < cols || !tol.is_finite() || tol <= 0.0 {
        return -1;
    }
    let slice = unsafe { std::slice::from_raw_parts_mut(w_ptr, len) };
    match newton_schulz_ord5_retract(slice, rows, cols, max_iters, tol) {
        Ok(def) => {
            unsafe { *out_defect = def; }
            0
        },
        Err(_) => -2
    }
}
