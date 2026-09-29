import json
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al PATH para importaciones locales
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Ruta al archivo de credenciales
_SECRETS_PATH = PROJECT_ROOT / ".secrets" / "api_keys.json"

def _load_key() -> str:
    """Carga la clave de OpenAI desde el archivo JSON seguro."""
    if not _SECRETS_PATH.is_file():
        raise FileNotFoundError(f"Credenciales OpenAI no encontradas en {_SECRETS_PATH}")
    with _SECRETS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    key = data.get("OPENAI_API_KEY")
    if not key:
        raise KeyError("La clave `OPENAI_API_KEY` no está presente en el archivo de credenciales.")
    return key

# Configuración global de la biblioteca oficial de OpenAI
import openai
openai.api_key = _load_key()

# Exportar el módulo configurado
__all__ = ["openai"]
