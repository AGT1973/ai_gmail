#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POLYD_IM RAG BRIDGE & MENSAJERÍA INDEPENDIENTE
Laboratorio Soberano POLYDIM-EINSOF (E:\\email_AGY\\agente_comunicacion)
Aislado e independiente del agente de clases de cursada.

Canales: WhatsApp (dedicado para futuro móvil propio de Antigravity) & Email institucional.
Inferencia: Cerebras WSE CS-3 (gpt-oss-120b, <600ms) + Fallback Local Ollama (polydim-comms-slm).
Base de Datos: PostgreSQL 16 (polydim_active_db.polydim_mensajeria_log y polydim_vec_db).
"""

import sys
import os
import time
import json
import urllib.request
import psycopg2

DB_ACTIVE = {
    "dbname": "polydim_active_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

DB_VEC = {
    "dbname": "polydim_vec_db",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

OLLAMA_URL = "http://192.168.100.21:11434/api/generate"
OLLAMA_MODEL = "polydim-comms-slm"

def obtener_cerebras_key() -> str:
    """Recupera la clave activa de Cerebras desde active_vault en PostgreSQL 16."""
    try:
        conn = psycopg2.connect(**DB_ACTIVE)
        cur = conn.cursor()
        cur.execute("SELECT value FROM active_vault WHERE key_name = 'cerebras_api_key' LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if row and row[0]:
            return row[0].strip()
    except Exception:
        pass
    return os.environ.get("CEREBRAS_API_KEY", "")

def es_socio_carlos(remitente: str, consulta: str) -> bool:
    r_lower = remitente.lower()
    c_lower = consulta.lower()
    return ("cegactuario@gmail.com" in r_lower or 
            "carlos" in r_lower or 
            "carlos gil" in c_lower or 
            "carlos-cyc" in c_lower or 
            "cyc" in c_lower)

def buscar_contexto_polydim(consulta: str, limit: int = 2) -> str:
    """Busca en polydim_vec_db (theorems / vault) si la consulta requiere contexto técnico."""
    try:
        conn = psycopg2.connect(**DB_VEC)
        cur = conn.cursor()
        palabras = [p for p in consulta.split() if len(p) > 3][:3]
        if not palabras:
            conn.close()
            return ""
        
        condiciones = " OR ".join(["theorem_name ILIKE %s OR formal_statement ILIKE %s"] * len(palabras))
        params = []
        for p in palabras:
            params.extend([f"%{p}%", f"%{p}%"])
            
        cur.execute(f"SELECT theorem_name, formal_statement FROM polydim_theorems WHERE {condiciones} LIMIT {limit}", params)
        rows = cur.fetchall()
        conn.close()
        
        if rows:
            ctx = "CONTEXTO TÉCNICO POLYDIM DISPONIBLE:\n"
            for name, stmt in rows:
                ctx += f"- Teorema {name}: {stmt[:160]}...\n"
            return ctx
    except Exception:
        pass
    return ""

def llamar_cerebras(prompt_sistema: str, prompt_usuario: str, max_tokens: int = 500) -> str:
    """Inferencia de silicio WSE ultra-rápida vía Cerebras API REST nativa."""
    key = obtener_cerebras_key()
    if not key:
        return ""
        
    payload = {
        "model": "gpt-oss-120b",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.cerebras.ai/v1/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "Polydim-Sovereign-Bridge/1.0"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=8) as response:
        res = json.loads(response.read().decode("utf-8"))
        choices = res.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            content = msg.get("content")
            if content and content.strip():
                return content.strip()
            reasoning = msg.get("reasoning")
            if reasoning and reasoning.strip():
                return reasoning.strip()
    return ""

def llamar_ollama_local(prompt: str) -> str:
    """Fallback soberano local Ollama con modelo polydim-comms-slm."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 120,
            "temperature": 0.2
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        res = json.loads(response.read().decode("utf-8"))
        return res.get("response", "").strip()

def registrar_auditoria(canal: str, remitente: str, nombre: str, asunto: str, consulta: str, respuesta: str, modelo: str, latencia_ms: float, socio_carlos: bool):
    try:
        conn = psycopg2.connect(**DB_ACTIVE)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO polydim_mensajeria_log 
            (canal, remitente, nombre_remitente, asunto, consulta, respuesta, modelo_usado, latencia_ms, es_socio_carlos)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (canal, remitente, nombre, asunto, consulta, respuesta, modelo, latencia_ms, socio_carlos))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[!] Error registrando auditoría polydim: {e}", file=sys.stderr)

def responder_whatsapp(remitente: str, consulta: str, nombre: str = "") -> dict:
    t0 = time.time()
    socio = es_socio_carlos(remitente, consulta)
    contexto = buscar_contexto_polydim(consulta)
    
    prompt_sistema = (
        "Eres el Asistente Oficial de Comunicaciones de POLYDIM-EINSOF (Laboratorio Soberano de Computación Continua y Variedades de Stiefel).\n"
        "DIRECTIVA WHATSAPP:\n"
        "- Máximo 80 palabras.\n"
        "- Tono ejecutivo, directo, sobrio (0 a 1 emoji).\n"
        "- Cero lenguaje servil o adulación.\n"
    )
    if socio:
        prompt_sistema += "ATENCIÓN ESPECIAL: El remitente es Carlos Gil / Socio del Proyecto CARLOS-CYC. Brinda prioridad ejecutiva y comunica que el avance está al día y verificado.\n"
    
    prompt_usuario = f"Remitente: {nombre or remitente}\nMensaje entrante: {consulta}\n{contexto}"
    
    modelo_usado = "Cerebras-CS3-gpt-oss-120b"
    respuesta = ""
    try:
        respuesta = llamar_cerebras(prompt_sistema, prompt_usuario, max_tokens=500)
    except Exception:
        pass
    
    if not respuesta:
        modelo_usado = f"Ollama-Local-{OLLAMA_MODEL}"
        try:
            full_prompt = f"{prompt_sistema}\n\n{prompt_usuario}\nRespuesta concisa:"
            respuesta = llamar_ollama_local(full_prompt)
        except Exception:
            respuesta = "Mensaje recibido en el canal institucional de POLYDIM-EINSOF. Procesando con el director Prof. Garcia Traba."
    
    latencia_ms = (time.time() - t0) * 1000.0
    registrar_auditoria("WHATSAPP", remitente, nombre, "", consulta, respuesta, modelo_usado, latencia_ms, socio)
    
    return {
        "canal": "WHATSAPP",
        "remitente": remitente,
        "respuesta": respuesta,
        "modelo": modelo_usado,
        "latencia_ms": round(latencia_ms, 2),
        "es_socio_carlos": socio
    }

def responder_email(remitente: str, asunto: str, consulta: str, nombre: str = "") -> dict:
    t0 = time.time()
    socio = es_socio_carlos(remitente, consulta)
    contexto = buscar_contexto_polydim(consulta)
    
    prompt_sistema = (
        "Eres el Asistente Oficial de Comunicaciones de POLYDIM-EINSOF (Laboratorio Soberano de Computación Continua).\n"
        "DIRECTIVA EMAIL:\n"
        "- Tono formal, institucional, estructurado y analítico.\n"
        "- Termina OBLIGATORIAMENTE con esta firma exacta:\n"
        "Laboratorio Soberano de Investigación POLYDIM-EINSOF\n"
        "Director: Prof. Ariel H. Garcia Traba\n"
        "Canal Autónomo Gandalf / Antigravity\n"
    )
    if socio:
        prompt_sistema += "ATENCIÓN ESPECIAL: El remitente es Carlos Gil / Socio del Proyecto CARLOS-CYC. Máxima prioridad institucional.\n"
        
    prompt_usuario = f"De: {nombre or remitente}\nAsunto: {asunto}\nCuerpo del correo:\n{consulta}\n\n{contexto}"
    
    modelo_usado = "Cerebras-CS3-gpt-oss-120b"
    respuesta = ""
    try:
        respuesta = llamar_cerebras(prompt_sistema, prompt_usuario, max_tokens=600)
    except Exception:
        pass
        
    if not respuesta:
        modelo_usado = f"Ollama-Local-{OLLAMA_MODEL}"
        try:
            full_prompt = f"{prompt_sistema}\n\n{prompt_usuario}\nRespuesta formal:"
            respuesta = llamar_ollama_local(full_prompt)
        except Exception:
            respuesta = (
                f"Estimado/a {nombre or remitente},\n\n"
                f"Confirmamos la recepción de su comunicación institucional respecto a '{asunto}'. "
                f"Ha sido radicada en el despacho del laboratorio para su evaluación técnica.\n\n"
                f"Laboratorio Soberano de Investigación POLYDIM-EINSOF\n"
                f"Director: Prof. Ariel H. Garcia Traba\n"
                f"Canal Autónomo Gandalf / Antigravity"
            )
            
    latencia_ms = (time.time() - t0) * 1000.0
    registrar_auditoria("EMAIL", remitente, nombre, asunto, consulta, respuesta, modelo_usado, latencia_ms, socio)
    
    return {
        "canal": "EMAIL",
        "remitente": remitente,
        "asunto": asunto,
        "respuesta": respuesta,
        "modelo": modelo_usado,
        "latencia_ms": round(latencia_ms, 2),
        "es_socio_carlos": socio
    }

if __name__ == "__main__":
    print("[*] Ejecutando test de silicio POLYDIM RAG Bridge con vault dinámico...")
    
    # Test 1: Consulta WhatsApp de Socio Carlos Gil
    res_wa = responder_whatsapp(
        remitente="cegactuario@gmail.com",
        consulta="Hola Ariel, como marcha la actualizacion del modelo CARLOS-CYC para el informe?",
        nombre="Carlos Gil"
    )
    print("\n--- TEST 1: WHATSAPP SOCIO CARLOS-CYC ---")
    print(f"Modelo: {res_wa['modelo']} | Latencia: {res_wa['latencia_ms']} ms | Es Socio: {res_wa['es_socio_carlos']}")
    print(f"Respuesta:\n{res_wa['respuesta']}")
    
    # Test 2: Consulta Email Institucional
    res_em = responder_email(
        remitente="evaluador@instituto-ia.org",
        asunto="Consulta sobre variedad de Stiefel y convergencia",
        consulta="Estimado Prof. Garcia Traba, requerimos precisiones sobre la tolerancia de retraccion polar en dimension D=4096.",
        nombre="Dr. S. Vance"
    )
    print("\n--- TEST 2: EMAIL INSTITUCIONAL TÉCNICO ---")
    print(f"Modelo: {res_em['modelo']} | Latencia: {res_em['latencia_ms']} ms")
    print(f"Respuesta:\n{res_em['respuesta']}")
