"""
Dynamic Model Probe & Capability Cataloger (Silicon Contract - Zero Hardcoding)
=============================================================================
Consulta en vivo las APIs de los proveedores activos (Cerebras, Groq, OpenRouter, etc.)
y genera un catálogo dinámico de cómputo para el enjambre de POLYDIM.
"""

import os
import json
import re
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"E:\email_AGY")
OUTPUT_CATALOG_EMAIL = BASE_DIR / "DYNAMIC_COMPUTE_CATALOG.json"
OUTPUT_CATALOG_POLYDIM = Path(r"E:\POLYDIM_EINSOF\DYNAMIC_COMPUTE_CATALOG.json")

def get_api_key(pattern, env_var=None):
    """Busca una API key en variables de entorno, .env_paid_keys o PERMANENT_MEMORY.md."""
    if env_var and os.environ.get(env_var):
        return os.environ.get(env_var)

    # Buscar en .env_paid_keys
    env_file = Path(r"C:\Users\eluithi\.gemini\config\.env_paid_keys")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if pattern in line and "=" in line:
                return line.split("=", 1)[1].strip()

    # Buscar en PERMANENT_MEMORY.md
    pm_file = Path(r"C:\Users\eluithi\.gemini\config\PERMANENT_MEMORY.md")
    if pm_file.exists():
        text = pm_file.read_text(encoding="utf-8")
        m = re.search(rf"({pattern}[a-zA-Z0-9_\-]+)", text)
        if m:
            return m.group(1)
            
    return None

def probe_cerebras():
    """Consulta modelos vivos en Cerebras WSE API."""
    key = get_api_key("csk-", "CEREBRAS_API_KEY")
    if not key:
        return {"status": "NO_KEY", "models": []}

    headers = {
        "Authorization": f"Bearer {key}",
        "User-Agent": "POLYDIM_DynamicProbe/1.0",
        "Content-Type": "application/json"
    }
    try:
        res = requests.get("https://api.cerebras.ai/v1/models", headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            models = [m.get("id") for m in data.get("data", []) if m.get("id")]
            return {
                "status": "ONLINE",
                "provider": "Cerebras Wafer-Scale (WSE)",
                "models": models,
                "fastest_qwen": next((m for m in models if "qwen" in m.lower()), None),
                "fastest_reasoner": next((m for m in models if "gpt-oss" in m.lower() or "llama" in m.lower()), None)
            }
        else:
            return {"status": f"HTTP_{res.status_code}", "models": [], "error": res.text[:200]}
    except Exception as e:
        return {"status": "ERROR", "models": [], "error": str(e)}

def probe_groq():
    """Consulta modelos vivos en Groq API."""
    key = get_api_key("gsk_", "GROQ_API_KEY")
    if not key:
        return {"status": "NO_KEY", "models": []}

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    try:
        res = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            models = [m.get("id") for m in data.get("data", []) if m.get("id")]
            return {
                "status": "ONLINE",
                "provider": "Groq LPU",
                "models": models,
                "sota_llama": next((m for m in models if "llama-3.3-70b" in m.lower() or "llama-3.1-70b" in m.lower()), None),
                "sota_deepseek": next((m for m in models if "deepseek-r1" in m.lower()), None)
            }
        else:
            return {"status": f"HTTP_{res.status_code}", "models": [], "error": res.text[:200]}
    except Exception as e:
        return {"status": "ERROR", "models": [], "error": str(e)}

def probe_openrouter():
    """Consulta modelos SOTA prioritarios en OpenRouter."""
    key = get_api_key("sk-or-v1-", "OPENROUTER_API_KEY")
    if not key:
        return {"status": "NO_KEY", "models": []}

    headers = {
        "Authorization": f"Bearer {key}",
        "HTTP-Referer": "https://github.com/AGT1973/POLYDIM",
        "X-Title": "POLYDIM Dynamic Probe"
    }
    try:
        res = requests.get("https://openrouter.ai/api/v1/models", headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            all_models = [m.get("id") for m in data.get("data", []) if m.get("id")]
            qwen_models = [m for m in all_models if "qwen" in m.lower()]
            deepseek_models = [m for m in all_models if "deepseek" in m.lower()]
            return {
                "status": "ONLINE",
                "provider": "OpenRouter Gateway",
                "total_models": len(all_models),
                "sota_qwen_cloud": qwen_models[0] if qwen_models else None,
                "sota_deepseek_cloud": deepseek_models[0] if deepseek_models else None
            }
        else:
            return {"status": f"HTTP_{res.status_code}", "models": []}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def update_catalog():
    """Ejecuta todos los sondeos y compila el catálogo dinámico de cómputo."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    catalog = {
        "last_probe_timestamp": ts,
        "providers": {
            "cerebras_wse": probe_cerebras(),
            "groq_lpu": probe_groq(),
            "openrouter_gateway": probe_openrouter()
        },
        "optimal_routing": {}
    }

    # Determinar ruteo óptimo dinámico (Zero Hardcoding)
    cerebras = catalog["providers"].get("cerebras_wse", {})
    groq = catalog["providers"].get("groq_lpu", {})
    openrouter = catalog["providers"].get("openrouter_gateway", {})

    # Qwen SOTA
    if cerebras.get("fastest_qwen"):
        catalog["optimal_routing"]["qwen"] = {
            "provider": "cerebras_wse",
            "model_id": cerebras["fastest_qwen"],
            "reason": "Inferencia nativa en oblea Cerebras WSE (baja latencia)"
        }
    elif openrouter.get("sota_qwen_cloud"):
        catalog["optimal_routing"]["qwen"] = {
            "provider": "openrouter_gateway",
            "model_id": openrouter["sota_qwen_cloud"],
            "reason": "Fallback OpenRouter cloud"
        }

    # Razonador rápido / Árbitro de Red Team
    if cerebras.get("fastest_reasoner"):
        catalog["optimal_routing"]["fast_arbitrator"] = {
            "provider": "cerebras_wse",
            "model_id": cerebras["fastest_reasoner"],
            "reason": "Árbitro formal a escala de oblea Cerebras WSE"
        }
    elif groq.get("sota_llama"):
        catalog["optimal_routing"]["fast_arbitrator"] = {
            "provider": "groq_lpu",
            "model_id": groq["sota_llama"],
            "reason": "Fallback Groq LPU"
        }

    # Guardar en ubicaciones del sistema
    catalog_json = json.dumps(catalog, indent=2, ensure_ascii=False)
    
    OUTPUT_CATALOG_EMAIL.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_CATALOG_EMAIL.write_text(catalog_json, encoding="utf-8")

    if OUTPUT_CATALOG_POLYDIM.parent.exists():
        OUTPUT_CATALOG_POLYDIM.write_text(catalog_json, encoding="utf-8")

    print(f"[{ts}] DYNAMIC MODEL PROBE: Catálogo actualizado con éxito.")
    print(f" -> Qwen óptimo: {catalog['optimal_routing'].get('qwen', {}).get('model_id')} ({catalog['optimal_routing'].get('qwen', {}).get('provider')})")
    print(f" -> Árbitro rápido: {catalog['optimal_routing'].get('fast_arbitrator', {}).get('model_id')} ({catalog['optimal_routing'].get('fast_arbitrator', {}).get('provider')})")
    return catalog

if __name__ == "__main__":
    update_catalog()
