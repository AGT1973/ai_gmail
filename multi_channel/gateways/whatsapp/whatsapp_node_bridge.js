/**
 * AGY WhatsApp Multi-Device Gateway (Headless via Baileys)
 * ========================================================
 * Permite que AGY use WhatsApp sin mantener un celular encendido.
 * Soporta autenticación por "Pairing Code" (código de 8 dígitos en terminal).
 */

import makeWASocket, {
    useMultiFileAuthState,
    DisconnectReason,
    fetchLatestBaileysVersion
} from '@whiskeysockets/baileys';
import pino from 'pino';
import readline from 'readline';
import path from 'path';
import { fileURLToPath } from 'url';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SESSIONS_DIR = path.resolve(__dirname, '../../sessions/whatsapp_auth');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const question = (text) => new Promise((resolve) => rl.question(text, resolve));

// Enviar texto al cerebro de Python vía HTTP local
async function askAGYBrain(senderId, senderName, text) {
    return new Promise((resolve) => {
        const postData = JSON.stringify({
            sender_id: senderId,
            sender_name: senderName,
            message: text,
            channel: 'whatsapp'
        });

        const req = http.request({
            hostname: '127.0.0.1',
            port: 5055,
            path: '/ask',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            },
            timeout: 20000
        }, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(data);
                    resolve(parsed.reply || parsed.text || '');
                } catch (e) {
                    resolve('');
                }
            });
        });

        req.on('error', () => {
            resolve('[AGY Local Gateway]: El núcleo cognitivo está procesando en cola o iniciando.');
        });

        req.write(postData);
        req.end();
    });
}

async function startWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState(SESSIONS_DIR);
    const { version, isLatest } = await fetchLatestBaileysVersion();

    console.log(`📡 Conectando a WhatsApp Web (v${version.join('.')}, isLatest: ${isLatest})...`);

    const sock = makeWASocket({
        version,
        logger: pino({ level: 'silent' }),
        printQRInTerminal: false,
        auth: state,
        browser: ['Antigravity AGY', 'Chrome', '124.0.0']
    });

    // Si no está registrado, pedir número y generar Pairing Code
    if (!sock.authState.creds.registered) {
        console.log('\n======================================================');
        console.log('📲 VINCULACION HEADLESS POR PAIRING CODE (SIN QR)');
        console.log('======================================================');
        console.log('En cuanto tengas el celular con el chip:');
        console.log('1. Abrí WhatsApp en el celular.');
        console.log('2. Menú de 3 puntos -> Dispositivos vinculados -> Vincular con número.');
        console.log('3. Ingresá el código de 8 dígitos que aparecerá aquí abajo.\n');

        const phoneNumber = await question('👉 Ingrese el número telefónico (ej: 5491144754637): ');
        const cleanNumber = phoneNumber.replace(/[^0-9]/g, '');

        try {
            const code = await sock.requestPairingCode(cleanNumber);
            console.log('\n' + '⭐'.repeat(30));
            console.log(`🔥 TU CODIGO DE VINCULACION ES:  ${code?.match(/.{1,4}/g)?.join('-') || code}`);
            console.log('⭐'.repeat(30) + '\n');
            console.log('⏳ Esperando confirmación desde el celular...');
        } catch (err) {
            console.error('❌ Error al solicitar código de vinculación:', err);
        }
    }

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect } = update;
        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut);
            console.log('⚠️ Conexión de WhatsApp cerrada. Reconectando:', shouldReconnect);
            if (shouldReconnect) {
                setTimeout(startWhatsApp, 3000);
            }
        } else if (connection === 'open') {
            console.log('\n🎉 ¡WHATSAPP DE AGY CONECTADO EXITOSAMENTE!');
            console.log('💾 Sesión guardada. Ya podés retirar el chip si lo deseás.');
            console.log('🤖 AGY está listo para recibir y responder chats en WhatsApp.\n');
        }
    });

    // Escuchar mensajes entrantes
    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        if (type !== 'notify') return;

        for (const msg of messages) {
            if (msg.key.fromMe) continue;
            const senderJid = msg.key.remoteJid;
            if (!senderJid || senderJid.includes('@broadcast')) continue;

            const text = msg.message?.conversation ||
                         msg.message?.extendedTextMessage?.text || '';

            if (!text.trim()) continue;

            const senderName = msg.pushName || senderJid.split('@')[0];
            console.log(`📩 [WPP IN] ${senderName} (${senderJid}): '${text}'`);

            // Marcar como visto y responder
            await sock.sendPresenceUpdate('composing', senderJid);
            const reply = await askAGYBrain(senderJid, senderName, text);

            if (reply) {
                await sock.sendMessage(senderJid, { text: reply });
                console.log(`📤 [WPP OUT -> ${senderName}]: ${reply.substring(0, 60)}...`);
            }
            await sock.sendPresenceUpdate('available', senderJid);
        }
    });
}

startWhatsApp().catch((err) => console.error('Error fatal en WhatsApp Bridge:', err));
