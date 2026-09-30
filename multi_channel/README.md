# 📡 AGY Multi-Channel Autonomous Identity (POLYDIM)

Este subsistema otorga a **Antigravity (AGY)** su propia presencia autónoma multicanal (**Telegram, WhatsApp y Discord**) con un número de teléfono celular asignado, **sin necesidad de mantener un teléfono físico encendido**.

---

## 🏗️ Arquitectura Headless

```
[ Usuario externo ] 
        │ (WhatsApp / Telegram / Discord)
        ▼
┌─────────────────────────────────────────────────────────────┐
│ E:\email_AGY\multi_channel\                                │
│                                                             │
│  ├─ gateways/                                               │
│  │    ├─ telegram_service.py   (MTProto Userbot con Telethon)│
│  │    ├─ whatsapp/             (Node.js Baileys PairingCode)│
│  │    └─ discord_service.py    (discord.py DM / Mentions)   │
│  │                                                          │
│  ├─ core/                                                   │
│  │    ├─ server_bridge.py      (HTTP 5055 local bridge)     │
│  │    └─ agy_brain.py          (Cerebras CS-3 11ms + Gemini)│
│  │                             (POLYDIM, Anti-Leak, Whitelist)
│  └─ sessions/                  (Credenciales locales fijas) │
└─────────────────────────────────────────────────────────────┘
```

* **Cero Bot Estático:** AGY responde en primera persona, con todo el conocimiento de POLYDIM ($S^{D-1}$, PMTP, C++/Rust, Clifford), rigor matemático y actitud crítica (Bulldog Mode).
* **Guardián Anti-Leak:** Reconoce automáticamente a los contactos prioritarios:
  - **Ariel García Traba (`+54 9 11 4475 4637`)** -> `CREATOR_ROOT`
  - **Kevin Piterman (`kevinpiterman@gmail.com`)** -> `ACADEMIC_COLLABORATOR`
  - **Emilio Rasic (`rasic.emilio@gmail.com`)** -> `ACADEMIC_COLLABORATOR`
  - Usuarios públicos -> Respuestas técnicas rigurosas sin filtrar claves ni código no publicado.

---

## 🚀 Activación en 60 Segundos (Cuando tengas el celular con el chip)

1. **Insertar el chip en el celular** durante 2 minutos para recibir los códigos de activación.
2. Abrir una terminal en `E:\email_AGY\multi_channel` y ejecutar:
   ```bash
   python bootstrap_wizard.py
   ```
3. Seleccionar la opción deseada:
   - **Opción [1] TELEGRAM:** Te pide el número, Telegram envía un SMS al celular, ingresás los 5 dígitos en la consola y la sesión queda grabada en `sessions/agy_telegram.session`.
   - **Opción [2] WHATSAPP:** En la consola aparecerá un código de emparejamiento de 8 dígitos (ej: `ABCD-1234`). En WhatsApp del celular vas a *Dispositivos vinculados -> Vincular con número de teléfono*, ingresás el código y la sesión se almacena en `sessions/whatsapp_auth/`.
4. **Listo:** Retirás el chip del celular. Ya no se necesita el celular nunca más.
5. Seleccionar **Opción [5] INICIAR TODOS LOS CANALES ACTIVOS** para dejar a AGY atendiendo 24/7.
