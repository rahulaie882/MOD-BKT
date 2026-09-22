const express = require('express');
const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Railway के Environment Variables से मास्टर टोकन और एडमिन आईडी ली जाएगी
const MASTER_TOKEN = process.env.MASTER_BOT_TOKEN;
const ADMIN_ID = process.env.ADMIN_ID; 

const bot = new TelegramBot(MASTER_TOKEN, { polling: true });

// लिंक सेव करने के लिए फाईल का रास्ता
const dbPath = path.join(__dirname, 'link.json');

// करंट लिंक प्राप्त करने का फंक्शन
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

// --- एक्सप्रेस सर्वर (Instagram Ads के लिए परमानेंट लिंक) ---
app.get('/start', (req, res) => {
    const currentUsername = getCurrentBotUsername();
    res.redirect(`https://t.me/${currentUsername}`);
});

app.get('/', (req, res) => {
    sendResponse(res, 'Dynamic Redirect Gateway is running!');
});

function sendResponse(res, message) {
    res.send(message);
}

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

// --- टेलीग्राम बोट कमांड (चैट से लिंक बदलने के लिए) ---
bot.onText(/\/setlink (.+)/, (msg, match) => {
    const chatId = msg.chat.id.toString();
    
    // चेक करें कि कमांड सिर्फ आप (Admin) ही चला रहे हैं
    if (checkAdmin(chatId, ADMIN_ID)) {
        let newUsername = match[1].trim();
        // अगर यूजरनेम में @ लगा है तो उसे हटा दें
        newUsername = newUsername.replace('@', '');

        // फाईल में नया बोट यूजरनेम सेव करें
        fs.writeFileSync(dbPath, JSON.stringify({ username: newUsername }));
        
        bot.sendMessage(chatId, `✅ Success! New bot link updated to: https://t.me/${newUsername}\n\nअब Instagram Ads वाले यूजर इसी नए बोट पर जाएंगे।`);
    } else {
        bot.sendMessage(chatId, "❌ You are not authorized to use this command.");
    }
});

function checkAdmin(id1, id2) {
    if (!id2) return true; // अगर एडमिन आईडी सेट नहीं है तो कोई भी चला सकता है
    return id1 === id2.toString();
}
