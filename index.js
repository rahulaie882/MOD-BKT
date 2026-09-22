const express = require('express');
const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// ==========================================
// Bot Token aur Admin Chat ID
// ==========================================
const MASTER_TOKEN = "8899607476:AAHXL3Yenp-fNcPpqytMbObf4j4RC08bCns"; 
const ADMIN_ID = "8963867689";     

app.use(express.json());

const bot = new TelegramBot(MASTER_TOKEN, { webHook: true });
const URL = 'https://babaseller.one';


// Webhook set karein
bot.setWebHook(`${URL}/bot${MASTER_TOKEN}`);

// Telegram webhook endpoint
app.post(`/bot${MASTER_TOKEN}`, (req, res) => {
    bot.processUpdate(req.body);
    res.sendStatus(200);
});

const dbPath = path.join(__dirname, 'link.json');

function getCurrentBotUsername() {
    try {
        if (fs.existsSync(dbPath)) {
            const data = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
            return data.username || 'NEW_VIIP_2_BOT';
        }
    } catch (err) {
        console.error("Read error:", err);
    }
    return 'NEW_VIIP_2_BOT';
}

// --- Express Server (Instagram Ads Link) ---
app.get('/start', (req, res) => {
    const currentUsername = getCurrentBotUsername();
    res.redirect(`https://t.me/${currentUsername}`);
});

app.get('/', (req, res) => {
    res.send('Dynamic Redirect Gateway (Webhook Mode) is running!');
});

// Railway ke liye 0.0.0.0 par bind karna zaroori hai taaki timeout na ho
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT}`);
});

// --- Bot Command: /start ---
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "🤖 **Master Control Panel Active**\n\nNaya bot link set karne ke liye is tarah bhejein:\n`/setlink aapka_naya_bot_username`", { parse_mode: "Markdown" });
});

// --- Bot Command: /setlink ---
bot.onText(/\/setlink(?:\s+https?:\/\/t\.me\/|\s+@|\s+)?([a-zA-Z0-9_]+)/, (msg, match) => {
    const chatId = msg.chat.id.toString();
    
    if (chatId === ADMIN_ID.toString()) {
        let newUsername = match[1].trim();

        fs.writeFileSync(dbPath, JSON.stringify({ username: newUsername }));
        
        bot.sendMessage(chatId, `✅ Success! New bot link updated to:\nhttps://t.me/${newUsername}\n\nAb Instagram Ads wale user isi naye bot par jayenge.`);
    } else {
        bot.sendMessage(chatId, "❌ You are not authorized to use this command.");
    }
});
            
