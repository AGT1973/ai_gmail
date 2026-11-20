import pymupdf
import os

pdf_rondas = r"E:/email_AGY/DOCUMENTACION/INFORMES_RAFAEL_KAGGLE/POLYDIM_EinsofOS_Informe_Rondas_v2_v3_v4_19Nov.pdf"
pdf_ronda5 = r"E:/email_AGY/DOCUMENTACION/INFORMES_RAFAEL_KAGGLE/POLYDIM_EinsofOS_Informe_Ronda_5_20Nov2026.pdf"

def extract_pdf(pdf_path, out_txt):
    doc = pymupdf.open(pdf_path)
    text = []
    text.append(f"# CONTENIDO DE: {os.path.basename(pdf_path)}\nTotal Páginas: {len(doc)}\n")
    for i, page in enumerate(doc):
        text.append(f"\n--- PÁGINA {i+1} ---\n")
        text.append(page.get_text())
    page_count = len(doc)
    doc.close()
    full_text = "\n".join(text)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"[OK] Extraído {os.path.basename(pdf_path)} -> {out_txt} ({len(full_text)} caracteres, {page_count} págs)")

extract_pdf(pdf_rondas, r"E:/email_AGY/DOCUMENTACION/INFORMES_RAFAEL_KAGGLE/EXTRACTO_RONDAS_v2_v3_v4.txt")
extract_pdf(pdf_ronda5, r"E:/email_AGY/DOCUMENTACION/INFORMES_RAFAEL_KAGGLE/EXTRACTO_RONDA_5.txt")
