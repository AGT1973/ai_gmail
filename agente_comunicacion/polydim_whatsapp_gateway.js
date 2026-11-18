/**
 * GATEWAY WHATSAPP EXCLUSIVO DE POLYDIM-EINSOF (FUTURO CELULAR PROPIO DE ANTIGRAVITY)
 * Laboratorio Soberano de Investigación POLYDIM-EINSOF (E:\email_AGY\agente_comunicacion)
 * 
 * Totalmente desacoplado de las cátedras y de E:\WHATSAPP.
 * Puerto: 5060
 * Autenticación: .wweb_auth_polydim
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const QRCode = require('qrcode');
const { spawn } = require('child_process');
const { Client, LocalAuth } = require('whatsapp-web.js');

const app = express();
const PORT = process.env.PORT || 5060;

app.use(cors());
app.use(express.json());

let isConnected = false;
let currentQrDataUrl = null;

// Configuración anti-detección puppeteer para WhatsApp Web en Windows
const client = new Client({
    authStrategy: new LocalAuth({ dataPath: path.join(__dirname, '.wweb_auth_polydim') }),
    webVersionCache: {
        type: 'remote',
        remotePath: 'https://raw.githubusercontent.com/wppconnect-team/wa-js/main/dist/wppconnect-wa.js'
    },
    puppeteer: {
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
            '--disable-blink-features=AutomationControlled',
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        ]
    }
});

client.on('qr', async (qr) => {
    console.log('[!] Nuevo QR generado para el Celular Propio de Antigravity / POLYDIM.');
    try {
        currentQrDataUrl = await QRCode.toDataURL(qr, { width: 260, margin: 1 });
        await QRCode.toFile(path.join(__dirname, 'polydim_whatsapp_qr.png'), qr, { width: 300, margin: 1 });
        console.log('[✓] Archivo QR guardado en polydim_whatsapp_qr.png listo para escanear.');
    } catch (err) {
        console.error('Error generando QR:', err);
    }
});

client.on('ready', () => {
    isConnected = true;
    currentQrDataUrl = null;
    console.log('[✓] ¡WHATSAPP POLYDIM VINCULADO Y OPERATIVO EN DISPOSITIVO PROPIO!');
});

client.on('authenticated', () => {
    console.log('[✓] Autenticación POLYDIM exitosa.');
});

client.on('auth_failure', (msg) => {
    console.error('[X] Fallo de autenticación en WhatsApp POLYDIM:', msg);
});

client.on('disconnected', (reason) => {
    isConnected = false;
    currentQrDataUrl = null;
    console.log('[X] WhatsApp POLYDIM desconectado:', reason);
});

// Procesamiento de mensajes entrantes a través de polydim_rag_bridge.py
function procesarMensajePolydim(sender, senderName, text, callback) {
    const pythonScript = path.join(__dirname, 'polydim_rag_bridge.py');
    const py = spawn('python', [
        '-c',
        `import sys, json; sys.path.insert(0, r"${__dirname}"); import polydim_rag_bridge; res = polydim_rag_bridge.responder_whatsapp(sys.argv[1], sys.argv[2], sys.argv[3]); print(json.dumps(res))`
        , sender, text, senderName
    ]);

    let output = '';
    py.stdout.on('data', (d) => { output += d.toString(); });
    py.on('close', (code) => {
        if (code === 0) {
            try {
                const parsed = JSON.parse(output.trim());
                callback(null, parsed.respuesta);
            } catch (e) {
                callback(e, null);
            }
        } else {
            callback(new Error(`Exit code ${code}`), null);
        }
    });
}

client.on('message', async (msg) => {
    if (msg.from.includes('@g.us') || msg.isStatus) return;

    try {
        const contact = await msg.getContact().catch(() => ({ pushname: msg.from }));
        const senderName = contact.pushname || msg.from;
        const incomingText = msg.body;

        console.log(`[📥 POLYDIM Mensaje]: De "${senderName}" (${msg.from}): "${incomingText}"`);

        procesarMensajePolydim(msg.from, senderName, incomingText, async (err, reply) => {
            if (!err && reply) {
                console.log(`[📤 POLYDIM Respuesta Enviada]: "${reply}"`);
                await msg.reply(reply);
            }
        });
    } catch (e) {
        console.error('Error procesando mensaje en WhatsApp POLYDIM:', e);
    }
});

app.get('/api/status', (req, res) => {
    res.json({
        service: "POLYDIM-EINSOF WhatsApp Gateway",
        phone_assignment: "Celular Propio Antigravity / Gandalf",
        connected: isConnected,
        port: PORT,
        qr: currentQrDataUrl
    });
});

app.listen(PORT, () => {
    console.log(`POLYDIM WHATSAPP GATEWAY (CELULAR PROPIO) ACTIVO EN: http://localhost:${PORT}`);
});

// Inicia el cliente WhatsApp
client.initialize().catch((err) => {
    console.warn('Inicialización de WhatsApp POLYDIM diferida:', err.message);
});
