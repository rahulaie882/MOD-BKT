const express = require('express');
const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// ==========================================
// अपना बोट टोकन और एडमिन चैट आईडी यहाँ डालें
// ==========================================
const MASTER_TOKEN = "8899607476:AAHsR3aON_Kj60gZRKcKPmErgw_-vXO_oyw"; 
const ADMIN_ID = "8963867689";     

const bot = new TelegramBot(MASTER_TOKEN, { polling: true });

const dbPath = path.join(__dirname, 'link.json');

function getCurrentBotUsername() {
    try {
        if (fs.existsSync(dbPath)) {
            const data = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
            return data.username || 'DefaultBotUsername';
        }
    } catch (err) {
        console.error("Read error:", err);
    }
    return 'DefaultBotUsername';
}

// --- एक्सप्रेस सर्वर (Instagram Ads लिंक) ---
app.get('/start', (req, res) => {
    const currentUsername = getCurrentBotUsername();
    res.redirect(`https://t.me/${currentUsername}`);
});

app.get('/', (req, res) => {
    res.send('Dynamic Redirect Gateway is running!');
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

// --- बोट कमांड: /start ---
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, "🤖 **Master Control Panel Active**\n\nनया बोट लिंक सेट करने के लिए इस तरह भेजें:\n`/setlink आपका_नया_बोट_यूजरनेम`", { parse_mode: "Markdown" });
});

// --- बोट कमांड: /setlink ---
bot.onText(/\/setlink (.+)/, (msg, match) => {
    const chatId = msg.chat.id.toString();
    
    if (chatId === ADMIN_ID.toString()) {
        let newUsername = match[1].trim();
        newUsername = newUsername.replace('@', '');

        fs.writeFileSync(dbPath, JSON.stringify({ username: newUsername }));
        
        bot.sendMessage(chatId, `✅ Success! New bot link updated to:\nhttps://t.me/${newUsername}\n\nअब Instagram Ads वाले यूजर इसी नए बोट पर जाएंगे।`);
    } else {
        bot.sendMessage(chatId, "❌ You are not authorized to use this command.");
    }
});
           
