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
BOT_TOKEN = "8892594189:AAE6ikOmt4WU65yCBXBNvzvtKzrixDngl2I"  # Testing Bot Token
ADMIN_ID = 8999416691  # Admin Telegram Numeric User ID

# --- API & VIDEO CONFIGURATION ---
NINEX_SETUP_VIDEO = "YAHAN_9X_SETUP_VIDEO_KA_LINK_DALNA"  # <-- Yahan apna 9X setup video link daal dena
BALA_SETUP_VIDEO = "https://files.catbox.moe/p1xt51.mp4"
BALA_DEMO_VIDEO = "https://files.catbox.moe/31m5me.mp4"
NINEX_DEMO_VIDEO = "https://files.catbox.moe/73gkqy.mp4"
SUPPORT_LINK = "https://t.me/VIDEO_GROUP_PURCHASE"

# Panel API Settings (optional - auto key generate)
PANEL_API_URL = "YAHAN_PANEL_KI_API_LINK_DALNA"
PANEL_API_KEY = "YAHAN_PANEL_KA_API_TOKEN_DALNA"


def generate_key_from_panel(duration_type):
    try:
        payload = {"api_key": PANEL_API_KEY, "duration": duration_type}
        response = requests.post(PANEL_API_URL, json=payload, timeout=10)
        data = response.json()
        if data.get("status") == "success":
            return data.get("key")
        return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None


# --- 1. /START COMMAND ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 BALA MOD", callback_data="mod_bala", style="danger")],
        [InlineKeyboardButton("🔵 NINE-X MOD", callback_data="mod_ninex", style="primary")],
        [InlineKeyboardButton("🎥 Watch Demo Videos", callback_data="show_demos", style="primary")],
        [InlineKeyboardButton("🎧 Support Team", url=SUPPORT_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "🏪 ━ JIBON MODS SHOP ━ 🏪\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "👋 Welcome, PREMIUM!\n\n"
        "⭐ ━ SHOP FEATURES ━ ⭐\n\n"
        "├ 🔑 Premium Game Keys\n"
        "├ ⚡ Instant Delivery 24/7\n"
        "├ 🔒 100% Secure Payment\n"
        "├ 💸 Best Prices Guaranteed\n"
        "├ 🎁 Referral Rewards\n"
        "└ 🏆 Professional Support\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🔥 Choose a mod below to check setup guides & pricing!\n\n"
        "👑 Official Support: @VIDEO_GROUP_PURCHASE"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        try:
            await update.callback_query.message.edit_text(
                welcome_text, reply_markup=reply_markup
            )
        except Exception:
            await update.callback_query.message.reply_text(
                welcome_text, reply_markup=reply_markup
            )


# --- 2. DEMO VIDEOS ---
async def show_demos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Send both demo videos
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=BALA_DEMO_VIDEO,
        caption="🔴 BALA-MOD Demo Video",
    )
    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=NINEX_DEMO_VIDEO,
        caption="🔵 NINE-X MOD Demo Video",
    )

    # Buttons below demos (vertical)
    keyboard = [
        [InlineKeyboardButton("🔴 BALA Setup & Prices", callback_data="mod_bala", style="danger")],
        [InlineKeyboardButton("🔵 NINE-X Setup & Prices", callback_data="mod_ninex", style="primary")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu", style="primary")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="👆 Demo videos upar hain.\n\nNeeche se Setup & Prices choose karo:",
        reply_markup=reply_markup,
    )


# --- 3. BALA MOD MENU (Setup Video + Price Buttons) ---
async def mod_bala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    caption = (
        "🔴 Free Fire Bala Mods Full Setup Video\n\n"
        "🚨 BALA MOD MENU — KEY AVAILABLE NOW! 🚨\n\n"
        "🎮 NON-ROOT MOD MENU\n"
        "✅ Main ID Safe\n"
        "⚡ Quick Key Delivery\n"
        "🔥 Multiple Duration Options\n\n"
        "Neeche se apna plan choose karo 👇"
    )

    # Saare buttons ek ke neeche ek (vertical)
    keyboard = [
        [InlineKeyboardButton("🔴 1 Hour  —  ₹35", callback_data="buy_bala_1h", style="danger")],
        [InlineKeyboardButton("🔴 3 Hours —  ₹80", callback_data="buy_bala_3h", style="danger")],
        [InlineKeyboardButton("🔴 6 Hours — ₹140", callback_data="buy_bala_6h", style="danger")],
        [InlineKeyboardButton("🔴 12 Hours — ₹240", callback_data="buy_bala_12h", style="danger")],
        [InlineKeyboardButton("🔴 24 Hours — ₹380", callback_data="buy_bala_24h", style="danger")],
        [InlineKeyboardButton("🔴 2 Days  — ₹650", callback_data="buy_bala_2d", style="danger")],
        [InlineKeyboardButton("🔴 3 Days  — ₹800", callback_data="buy_bala_3d", style="danger")],
        [InlineKeyboardButton("🔙 Back to Demos", callback_data="show_demos", style="primary")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu", style="primary")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_video(
        chat_id=query.message.chat_id,
        video=BALA_SETUP_VIDEO,
        caption=caption,
        reply_markup=reply_markup,
    )


# --- 4. NINE-X MOD MENU ---
async def mod_ninex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    caption = (
        "🔵 NINE-X MOD SETUP & PRICING\n\n"
        "⏱️ Duration: 10 Days\n"
        "💵 Price: ₹500\n\n"
        "Setup video dekh lo carefully, phir neeche se purchase karo."
    )

    keyboard = [
        [InlineKeyboardButton("🔵 Purchase 10-Day Key — ₹500", callback_data="buy_ninex_10d", style="primary")],
        [InlineKeyboardButton("🔙 Back to Demos", callback_data="show_demos", style="primary")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu", style="primary")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Agar video link abhi nahi hai to message bhej do
    if NINEX_SETUP_VIDEO.startswith("YAHAN_"):
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=caption + "\n\n⚠️ Setup video abhi add nahi hua. Jaldi add ho jayega.",
            reply_markup=reply_markup,
        )
    else:
        await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=NINEX_SETUP_VIDEO,
            caption=caption,
            reply_markup=reply_markup,
        )


# --- 5. PAYMENT FLOW (QR + I Have Paid) ---
async def payment_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data.replace("buy_", "").upper()
    context.user_data["selected_plan"] = plan

    # Plan ka readable name
    plan_names = {
        "BALA_1H": "Bala Mod — 1 Hour (₹35)",
        "BALA_3H": "Bala Mod — 3 Hours (₹80)",
        "BALA_6H": "Bala Mod — 6 Hours (₹140)",
        "BALA_12H": "Bala Mod — 12 Hours (₹240)",
        "BALA_24H": "Bala Mod — 24 Hours (₹380)",
        "BALA_2D": "Bala Mod — 2 Days (₹650)",
        "BALA_3D": "Bala Mod — 3 Days (₹800)",
        "NINEX_10D": "Nine-X Mod — 10 Days (₹500)",
    }
    plan_display = plan_names.get(plan, plan)

    qr_caption = (
        f"💳 Payment Page\n\n"
        f"📦 Plan: {plan_display}\n\n"
        "1️⃣ Scan the QR code ya UPI se payment karo\n"
        "2️⃣ Exact amount bhejo\n"
        "3️⃣ Neeche ✅ I Have Paid dabao\n"
        "4️⃣ Payment screenshot bhejo\n\n"
        f"🎧 Support: {SUPPORT_LINK}"
    )

    keyboard = [
        [InlineKeyboardButton("✅ I Have Paid", callback_data="i_have_paid", style="success")],
        [InlineKeyboardButton("🎧 Support Team", url=SUPPORT_LINK)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu", style="primary")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # QR placeholder (apna real QR image link daal dena)
    qr_image_url = "https://i.ibb.co/6P2n1rd/qr-placeholder.png"

    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=qr_image_url,
        caption=qr_caption,
        reply_markup=reply_markup,
    )


# --- 6. I HAVE PAID → Screenshot maango ---
async def i_have_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["waiting_for_screenshot"] = True

    text = (
        "📸 Payment Screenshot Required\n\n"
        "Ab is chat mein apna Payment Screenshot bhejo.\n\n"
        "Screenshot aate hi system verify karega aur key deliver ho jayegi.\n"
        "Please wait..."
    )
    await query.message.reply_text(text)


# --- 7. SCREENSHOT HANDLE ---
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_screenshot"):
        return

    user = update.effective_user
    plan = context.user_data.get("selected_plan", "UNKNOWN")

    plan_names = {
        "BALA_1H": "Bala Mod — 1 Hour (₹35)",
        "BALA_3H": "Bala Mod — 3 Hours (₹80)",
        "BALA_6H": "Bala Mod — 6 Hours (₹140)",
        "BALA_12H": "Bala Mod — 12 Hours (₹240)",
        "BALA_24H": "Bala Mod — 24 Hours (₹380)",
        "BALA_2D": "Bala Mod — 2 Days (₹650)",
        "BALA_3D": "Bala Mod — 3 Days (₹800)",
        "NINEX_10D": "Nine-X Mod — 10 Days (₹500)",
    }
    plan_display = plan_names.get(plan, plan)

    # Admin ko screenshot + details bhejo
    forward_caption = (
        f"🔔 New Payment Proof Received!\n\n"
        f"👤 User: {user.full_name}\n"
        f"🔗 Username: @{user.username or 'No Username'}\n"
        f"🆔 User ID: `{user.id}`\n"
        f"📦 Plan: {plan_display}\n\n"
        f"Key bhejne ke liye:\n"
        f"`/sendkey {user.id} YOUR_KEY_HERE`"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=forward_caption,
        parse_mode="Markdown",
    )

    context.user_data["waiting_for_screenshot"] = False

    # User ko message
    await update.message.reply_text(
        "✅ Screenshot successfully received!\n\n"
        "⏳ Please wait...\n"
        "Aapka key jald hi is bot mein deliver ho jayega.\n\n"
        "Admin verify karke key bhej dega.\n"
        "Dhanyavaad! 🙏"
    )


# --- 8. ADMIN COMMAND: /sendkey <userid> <key> ---
async def send_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized to use this command.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ Usage:\n`/sendkey <UserID> <KEY>`\n\n"
            "Example:\n`/sendkey 123456789 ABCD-1234-XYZ`",
            parse_mode="Markdown",
        )
        return

    target_user_id = context.args[0]
    key_value = " ".join(context.args[1:])

    # Beautiful Bill
    bill_message = (
        "🎉 ━━━━━━━━━━━━━━━━━━━ 🎉\n"
        "     PAYMENT APPROVED\n"
        "🎉 ━━━━━━━━━━━━━━━━━━━ 🎉\n\n"
        f"🔑 Your Activation Key:\n"
        f"`{key_value}`\n\n"
        "--------------------------------\n"
        "📖 HOW TO USE:\n"
        "1. Copy the key above\n"
        "2. Open the game & paste in mod menu\n"
        "3. Enjoy safe gameplay!\n"
        "--------------------------------\n\n"
        "✅ Thanks for your purchase!\n"
        "🙏 We hope you enjoy the mod.\n\n"
        "⚠️ Do not share your key with anyone.\n"
        f"🎧 Support: {SUPPORT_LINK}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "JIBON MODS SHOP • Premium Quality"
    )

    try:
        await context.bot.send_message(
            chat_id=target_user_id,
            text=bill_message,
            parse_mode="Markdown",
        )
        await update.message.reply_text(
            f"✅ Key successfully sent to User ID: {target_user_id}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to send key.\nError: {e}")


# --- MAIN ---
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
    application.add_handler(CallbackQueryHandler(mod_bala, pattern="^mod_bala$"))
    application.add_handler(CallbackQueryHandler(mod_ninex, pattern="^mod_ninex$"))
    application.add_handler(CallbackQueryHandler(payment_flow, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(i_have_paid, pattern="^i_have_paid$"))

    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    logger.info("Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
