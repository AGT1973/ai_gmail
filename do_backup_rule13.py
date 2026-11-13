import shutil
import os

files_to_drive = [
    (r"E:\POLYDIM_EINSOF\DOCUMENTOS_MAESTROS\DIMENSION_IS_ALL_YOU_NEED_PAPER_V1550_HARDENED.md", r"G:\Mi unidad\01_PAPERS_Y_TEORIA_FORMAL"),
    (r"E:\POLYDIM_EINSOF\teoria\POLYDIM_EINSOFOS_ENTERPRISE_WHITEBOOK_V1550.md", r"G:\Mi unidad\01_PAPERS_Y_TEORIA_FORMAL"),
    (r"E:\POLYDIM_EINSOF\DESCRIPCION_EXPERIMENTOS_CUANTICOS_PUERTA_ADENTRO.md", r"G:\Mi unidad\04_EVIDENCIA_SILICIO_Y_CERTIFICACIONES"),
    (r"E:\POLYDIM_EINSOF\MODELOS_ESTADISTICOS_QPU_SOTA_PERPLEXITY.md", r"G:\Mi unidad\04_EVIDENCIA_SILICIO_Y_CERTIFICACIONES")
]

for src, dst_folder in files_to_drive:
    if os.path.exists(src) and os.path.exists(dst_folder):
        dst = os.path.join(dst_folder, os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"[OK G-Drive] {os.path.basename(src)} -> {dst_folder}")
    else:
        print(f"[WARN G-Drive] Not found: {src} or {dst_folder}")

# Backup a F:
backup_f = r"F:\Entrega_2026_11_03_CUANTICA"
os.makedirs(backup_f, exist_ok=True)
for src, _ in files_to_drive:
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(backup_f, os.path.basename(src)))
        print(f"[OK F-Drive] {os.path.basename(src)} -> {backup_f}")

print("\nBackup físico completado.")
