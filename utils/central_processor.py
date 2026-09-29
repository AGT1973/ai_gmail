def procesar_con_ia(platform: str, sender: str, texto: str):
    """Hook to the central AI pipeline.

    Args:
        platform: "Gmail", "Telegram", or "WhatsApp"
        sender: email address, Telegram user ID, or WhatsApp phone number
        texto: raw message text
    """
    # Placeholder: integrate with the real IA processing (OpenAI, Kimi, etc.)
    print(f"\n--- {platform.upper()} NUEVO de {sender}: {texto[:80]}...")
    
    # 📬 PROTOCOLO ESPECIAL KEVIN PITERMAN (kevinpiterman@gmail.com)
    if "kevinpiterman@gmail.com" in sender.lower():
        print("  [PROTOCOLO KEVIN PITERMAN ACTIVADO]")
        print("  -> Generando narrativa de 6 meses de POLYDIM (S^(D-1), PMTP Zero-Copy, C++/Rust).")
        print("  -> Verificando guardrails: Cero datos privados, formulas legibles en KaTeX.")
        
        # Detectar si solicita adjuntos o archivos
        keywords_adjuntos = ["adjunto", "archivo", "código", "codigo", "repositorio", "zip", "paper", "pdf", "attachment", "file"]
        pide_adjuntos = any(k in texto.lower() for k in keywords_adjuntos)
        
        if pide_adjuntos:
            print("  -> [VETO DE ENVIO AUTOMATICO] Solicitud de adjuntos/archivos detectada.")
            print("  -> ACCION: Guardando respuesta como BORRADOR (Draft). Requiere evaluacion humana de Ariel.")
        else:
            print("  -> Respuesta de consulta teorica preparada.")
