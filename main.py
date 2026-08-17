import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = "8892594189:AAGn3zxtbZpqkrJ_r-1SDjFILQDRsSPXQ7k"  # Apna Telegram Bot Token
ADMIN_ID = 8999416691  # Apni Telegram Numeric User ID

# --- API & VIDEO CONFIGURATION ---
NINEX_SETUP_VIDEO = "YAHAN_9X_SETUP_VIDEO_KA_LINK_DALNA"  # Baad mein link daal dena
BALA_SETUP_VIDEO = "https://files.catbox.moe/p1xt51.mp4"
BALA_DEMO_VIDEO = "https://files.catbox.moe/31m5me.mp4"
NINEX_DEMO_VIDEO = "https://files.catbox.moe/73gkqy.mp4"
SUPPORT_LINK = "https://t.me/VIDEO_GROUP_PURCHASE"

# Panel API Settings (Jahan se automatic key generate hogi)
PANEL_API_URL = "YAHAN_PANEL_KI_API_LINK_DALNA"
PANEL_API_KEY = "YAHAN_PANEL_KA_API_TOKEN_DALNA"


# Function to generate key automatically via Panel API
def generate_key_from_panel(duration_type):
    try:
        payload = {"api_key": PANEL_API_KEY, "duration": duration_type}
        response = requests.post(PANEL_API_URL, json=payload, timeout=10)
        data = response.json()
        if data.get("status") == "success":
            return data.get("key")
        else:
            return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None


# --- 1. /START COMMAND (CUSTOM JIBON MODS SHOP DESIGN) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔴 BALA MOD", callback_data="mod_bala"),
            InlineKeyboardButton("🔵 NINE-X MOD", callback_data="mod_ninex"),
        ],
        [InlineKeyboardButton("🎥 Watch Demo Videos", callback_data="show_demos")],
        [InlineKeyboardButton("🎧 Support Team", url=SUPPORT_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "🏪 ━ BABA MODS SHOP ━ 🏪\n"
        "  ━━━━━━━━━━━━━━━━━━\n\n"
        "👋 Welcome, 𝗣𝗥𝗘𝗠𝗜𝗨𝗠!\n\n"
        "⭐ ━ SHOP FEATURES ━ ⭐\n\n"
        "├ 🔑 Premium Game Keys\n"
        "├ ⚡ Instant Delivery 24/7\n"
        "├ 🔒 100% Secure Payment\n"
        "├ 💸 Best Prices Guaranteed\n"
        "├ 🎁 Referral Rewards\n"
        "└ 🏆 Professional Support\n\n"
        "  ━━━━━━━━━━━━━━━━━━\n"
        "🔥 *Choose a mod below to check setup guides & pricing!*\n\n"
        "👑 *Official Support:* @VIDEO_GROUP_PURCHASE"
    )

    if update.message:
        await update.message.reply_text(
            welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
        )


# --- 2. DEMO VIDEOS HANDLER ---
async def show_demos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🔴 BALA Setup & Prices", callback_data="mod_bala"),
            InlineKeyboardButton("🔵 NINE-X Setup & Prices", callback_data="mod_ninex"),
        ],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=BALA_DEMO_VIDEO,
        caption="🎮 *BALA-MOD Demo Video*",
        parse_mode="Markdown",
    )
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=NINEX_DEMO_VIDEO,
        caption="🔥 *NINE-X MOD Demo Video*\n\nChoose an option below to proceed:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


# --- 3. MOD SELECTION (BALA OR NINE-X) ---
async def mod_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "mod_bala":
        caption = (
            "👿 *Free Fire Bala Mods Full Setup Video*\n\n"
            "🚨 *BALA MOD MENU — KEY AVAILABLE NOW!* 🚨\n\n"
            "🎮 *NON-ROOT MOD MENU*\n"
            "✅ Main ID Safe\n"
            "⚡ Quick Key Delivery\n"
            "🔥 Multiple Duration Options"
        )
        keyboard = [
            [
                InlineKeyboardButton("1H (₹35)", callback_data="buy_bala_1h"),
                InlineKeyboardButton("3H (₹80)", callback_data="buy_bala_3h"),
            ],
            [
                InlineKeyboardButton("6H (₹140)", callback_data="buy_bala_6h"),
                InlineKeyboardButton("12H (₹240)", callback_data="buy_bala_12h"),
            ],
            [InlineKeyboardButton("24H (₹380)", callback_data="buy_bala_24h")],
            [
                InlineKeyboardButton("2D (₹650)", callback_data="buy_bala_2d"),
                InlineKeyboardButton("3D (₹800)", callback_data="buy_bala_3d"),
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="show_demos"),
                InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=BALA_SETUP_VIDEO,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    elif data == "mod_ninex":
        caption = (
            "🔥 *NINE-X MOD SETUP & PRICING*\n\n"
            "⏱️ *Duration:* 10 Days\n"
            "💵 *Price:* ₹500\n\n"
            "Watch the setup guide above carefully, then click below to purchase your key."
        )
        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Purchase 10-Day Key - ₹500", callback_data="buy_ninex_10d"
                )
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="show_demos"),
                InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=NINEX_SETUP_VIDEO,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )


# --- 4. PAYMENT & QR CODE FLOW ---
async def payment_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data.replace("buy_", "").upper()
    context.user_data["selected_plan"] = plan

    qr_caption = (
        f"💳 *Payment Page ({plan})*\n\n"
        "1. Scan the QR code or pay to the UPI ID.\n"
        "2. Send the exact amount.\n"
        "3. Click *'✅ I Have Paid'* and send your payment screenshot.\n\n"
        f"🎧 *Support / Admin:* {SUPPORT_LINK}"
    )

    keyboard = [
        [InlineKeyboardButton("✅ I Have Paid", callback_data="i_have_paid")],
        [InlineKeyboardButton("🎧 Support Team", url=SUPPORT_LINK)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    qr_image_url = "https://i.ibb.co/6P2n1rd/qr-placeholder.png"

    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=qr_image_url,
        caption=qr_caption,
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


# --- 5. "I HAVE PAID" TRIGGER ---
async def i_have_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["waiting_for_screenshot"] = True
    text = (
        "📸 *Payment Screenshot Required*\n\n"
        "Please send your **Payment Screenshot** right here in this chat.\n"
        "Our system will verify it and deliver your key!"
    )
    await query.message.edit_text(text, parse_mode="Markdown")


# --- 6. HANDLE SCREENSHOT & AUTO API KEY DELIVERY ---
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_screenshot"):
        user = update.effective_user
        plan = context.user_data.get("selected_plan", "MOD")

        forward_caption = (
            f"🔔 *New Payment Proof Received!*\n\n"
            f"👤 *User:* {user.full_name} (@{user.username or 'No Username'})\n"
            f"🆔 *User ID:* `{user.id}`\n"
            f"📦 *Plan:* {plan}"
        )
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=forward_caption,
            parse_mode="Markdown",
        )

        context.user_data["waiting_for_screenshot"] = False
        await update.message.reply_text(
            "⏳ *Payment Received!* Generating your key via API...",
            parse_mode="Markdown",
        )

        generated_key = generate_key_from_panel(plan)

        if generated_key:
            bill_message = (
                f"🎉 *PAYMENT APPROVED & KEY DELIVERED!* 🎉\n\n"
                f"--------------------------------------------\n"
                f"🔑 *Your Key:* `{generated_key}`\n"
                f"📅 *Plan:* {plan}\n"
                f"--------------------------------------------\n\n"
                f"📖 *HOW TO USE:*\n"
                f"1. Copy your activation key above.\n"
                f"2. Open the game & paste the key in the mod menu.\n"
                f"3. Enjoy your safe gameplay!\n\n"
                f"⚠️ *Note:* Do not share your key with anyone.\n"
                f"🎧 *Support:* {SUPPORT_LINK}"
            )
            await update.message.reply_text(bill_message, parse_mode="Markdown")
        else:
            await update.message.reply_text(
                "✅ Screenshot submitted! Admin will verify and send your key shortly.",
                parse_mode="Markdown",
            )
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"⚠️ *API Key Generation Failed for User `{user.id}`!* Please send key manually using `/sendkey`",
                parse_mode="Markdown",
            )


# --- 7. BACKUP MANUAL ADMIN COMMAND: /sendkey ---
async def send_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ You are not authorized to use this command."
        )
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ Usage: `/sendkey [UserID] [KEY]`", parse_mode="Markdown"
        )
        return

    target_user_id = context.args[0]
    key_value = " ".join(context.args[1:])

    bill_message = (
        f"🎉 *PAYMENT APPROVED & KEY DELIVERED!* 🎉\n\n"
        f"--------------------------------------------\n"
        f"🔑 *Your Key:* `{key_value}`\n"
        f"--------------------------------------------\n\n"
        f"📖 *HOW TO USE:*\n"
        f"1. Copy your activation key above.\n"
        f"2. Open the game & paste the key in the mod menu.\n"
        f"3. Enjoy your safe gameplay!\n\n"
        f"⚠️ *Note:* Do not share your key with anyone.\n"
        f"🎧 *Support:* {SUPPORT_LINK}"
    )

    try:
        await context.bot.send_message(
            chat_id=target_user_id, text=bill_message, parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Key sent successfully to the user!")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to send key. Error: {e}")


# --- MAIN APPLICATION SETUP ---
def main():
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .read_timeout(60)
        .write_timeout(60)
        .connect_timeout(60)
        .pool_timeout(60)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendkey", send_key))

    application.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(show_demos, pattern="^show_demos$"))
    application.add_handler(
        CallbackQueryHandler(mod_menu, pattern="^mod_(bala|ninex)$")
    )
    application.add_handler(CallbackQueryHandler(payment_flow, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(i_have_paid, pattern="^i_have_paid$"))

    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    logger.info("Bot is running with Jibon Mods Shop design...")
    application.run_polling()


if __name__ == "__main__":
    main()
  
