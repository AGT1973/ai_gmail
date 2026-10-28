#ifndef PMTP_WIN_SHM_H
#define PMTP_WIN_SHM_H

#ifdef _WIN32
#include <windows.h>
#include <stdio.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    HANDLE hMapFile;
    void*  pData;
    size_t total_size;
    int    is_owner;
} pmtp_win_shm_handle_t;

static inline int pmtp_win_shm_create_or_open(
    const char* name, 
    size_t size, 
    int create_new, 
    pmtp_win_shm_handle_t* out_h
) {
    if (!name || !out_h || size == 0) return -1;
    out_h->hMapFile = NULL;
    out_h->pData = NULL;
    out_h->total_size = size;
    out_h->is_owner = create_new;

    DWORD size_high = (DWORD)((size >> 32) & 0xFFFFFFFF);
    DWORD size_low  = (DWORD)(size & 0xFFFFFFFF);

    if (create_new) {
        // Create exclusive or open
        out_h->hMapFile = CreateFileMappingA(
            INVALID_HANDLE_VALUE,
            NULL,
            PAGE_READWRITE,
            size_high,
            size_low,
            name
        );
        if (out_h->hMapFile == NULL) return -2;
        if (GetLastError() == ERROR_ALREADY_EXISTS) {
            /* create_new means exclusive creation. Never reinterpret an existing mapping
               as a newly created slab or return it with unchecked dimensions/dtype. */
            CloseHandle(out_h->hMapFile);
            out_h->hMapFile = NULL;
            out_h->is_owner = 0;
            return -5;
        }
        out_h->is_owner = 1; // Brand new mapping only
    } else {
        out_h->hMapFile = OpenFileMappingA(
            FILE_MAP_ALL_ACCESS,
            FALSE,
            name
        );
        if (out_h->hMapFile == NULL) return -3;
    }

    /* Attached peers are deliberately read-write for compatibility with atomic lease counters */
    DWORD access = FILE_MAP_ALL_ACCESS;
    out_h->pData = MapViewOfFile(
        out_h->hMapFile,
        access,
        0,
        0,
        size
    );

    if (out_h->pData == NULL) {
        CloseHandle(out_h->hMapFile);
        out_h->hMapFile = NULL;
        return -4;
    }

    return 0;
}

static inline void pmtp_win_shm_close(pmtp_win_shm_handle_t* h) {
    if (!h) return;
    h->is_owner = 0;
    h->total_size = 0;
    if (h->pData) {
        UnmapViewOfFile(h->pData);
        h->pData = NULL;
    }
    if (h->hMapFile) {
        CloseHandle(h->hMapFile);
        h->hMapFile = NULL;
    }
}

#ifdef __cplusplus
}
#endif

#endif // _WIN32

#endif // PMTP_WIN_SHM_H
