"""
Prune and Extract Links from Old Emails (> 7 days)
==================================================
1. Identifica correos con más de 7 días de antigüedad en _HISTORICO_MAIL y AGENT_INBOX.
2. Extrae enlaces técnicos relevantes (GitHub, arXiv, AI tools, papers, documentación).
3. Consolida los enlaces en E:\\email_AGY\\ENLACES_INTERESANTES_MAIL.md.
4. Borra los archivos .md viejos de disco para liberar espacio y evitar basura.
"""

import os
import re
import email.utils
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(r"E:\email_AGY")
HISTORICO_DIR = BASE_DIR / "_HISTORICO_MAIL"
INBOX_DIR = BASE_DIR / "AGENT_INBOX"
LINKS_VAULT = BASE_DIR / "ENLACES_INTERESANTES_MAIL.md"

# Patrones de links basura / tracking que NO aportan valor
IGNORE_PATTERNS = [
    r"unsubscribe", r"cancelar", r"optout", r"privacy", r"privacidad",
    r"facebook\.com", r"twitter\.com", r"x\.com", r"instagram\.com",
    r"youtube\.com/channel", r"linkedin\.com/company", r"maps/search"
]

# Patrones de links relevantes / técnicos
TECH_PATTERNS = [
    r"github\.com", r"arxiv\.org", r"huggingface\.co", r"kaggle\.com",
    r"cerebras\.ai", r"cerebras\.net", r"ollama\.com", r"openai\.com",
    r"anthropic\.com", r"deepmind\.google", r"ai\.google", r"google\.com/cloud",
    r"docs\.", r"paper", r"article", r"research", r"competition", r"course", r"guide"
]

def is_interesting_url(url):
    url_lower = url.lower()
    for ign in IGNORE_PATTERNS:
        if re.search(ign, url_lower):
            return False
    for tech in TECH_PATTERNS:
        if re.search(tech, url_lower):
            return True
    return False

def parse_date(date_str):
    try:
        parsed = email.utils.parsedate_to_datetime(date_str)
        return parsed
    except Exception:
        pass
    try:
        # Formato ISO simple o timestamp
        clean_date = date_str.split('.')[0].strip()
        return datetime.fromisoformat(clean_date)
    except Exception:
        return None

def prune_and_extract():
    now = datetime.now(timezone.utc)
    one_week_ago = now - timedelta(days=7)

    files_to_check = []
    if HISTORICO_DIR.exists():
        files_to_check.extend(HISTORICO_DIR.glob("*.md"))
    if INBOX_DIR.exists():
        files_to_check.extend(INBOX_DIR.glob("*.md"))

    extracted_links = []
    deleted_count = 0
    preserved_count = 0

    for file_path in files_to_check:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            
            # Extraer headers
            m_date = re.search(r"\*\*Fecha:\*\*\s*(.+)", content)
            m_from = re.search(r"\*\*De:\*\*\s*(.+)", content)
            m_subj = re.search(r"\*\*Asunto:\*\*\s*(.+)", content)
            m_acc = re.search(r"\*\*Cuenta:\*\*\s*(.+)", content)

            date_raw = m_date.group(1).strip() if m_date else ""
            sender = m_from.group(1).strip() if m_from else "Desconocido"
            subject = m_subj.group(1).strip() if m_subj else "Sin Asunto"
            account = m_acc.group(1).strip() if m_acc else ""

            dt = parse_date(date_raw)
            
            # Si no se pudo parsear fecha o es menor a 7 días, preservar
            if not dt:
                preserved_count += 1
                continue
                
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            # Si tiene más de 7 días -> Procesar y borrar
            if dt < one_week_ago:
                # Extraer URLs
                urls = re.findall(r'https?://[^\s<>"\)\]]+', content)
                unique_interesting = list({u for u in urls if is_interesting_url(u)})

                if unique_interesting:
                    extracted_links.append({
                        "date": dt.strftime("%Y-%m-%d"),
                        "account": account,
                        "from": sender,
                        "subject": subject,
                        "urls": unique_interesting
                    })

                # Borrar archivo físico viejo
                file_path.unlink()
                deleted_count += 1
            else:
                preserved_count += 1

        except Exception as e:
            print(f"Error procesando {file_path.name}: {e}")

    # Guardar / anexar enlaces al archivo consolidado
    if extracted_links:
        header = ""
        if not LINKS_VAULT.exists():
            header = "# 🔗 Bóveda de Enlaces Interesantes Extraídos de Correos\n\n"
            header += "> Enlaces técnicos, repositorios y recursos extraídos automáticamente antes de purgar correos viejos (> 7 días).\n\n---\n\n"
        
        with open(LINKS_VAULT, "a", encoding="utf-8") as f:
            if header:
                f.write(header)
            for item in extracted_links:
                f.write(f"### [{item['date']}] {item['subject']}\n")
                f.write(f"- **De:** `{item['from']}` | **Cuenta:** `{item['account']}`\n")
                f.write("- **Enlaces destacados:**\n")
                for u in item['urls']:
                    f.write(f"  - <{u}>\n")
                f.write("\n")

    print(f"RESUMEN PURGA:")
    print(f" -> Correos con >7 días eliminados: {deleted_count}")
    print(f" -> Correos recientes preservados: {preserved_count}")
    print(f" -> Grupos de enlaces técnicos guardados en ENLACES_INTERESANTES_MAIL.md: {len(extracted_links)}")

if __name__ == "__main__":
    prune_and_extract()
