import logging
import json
import os
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

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CONFIG ---
BOT_TOKEN = "8892594189:AAE6ikOmt4WU65yCBXBNvzvtKzrixDngl2I"
ADMIN_ID = 8999416691
SUPPORT_LINK = "https://t.me/VIDEO_GROUP_PURCHASE"

# Fallback URLs (agar file_id nahi hai to)
FALLBACK_BALA_SETUP = "https://files.catbox.moe/p1xt51.mp4"
FALLBACK_BALA_DEMO = "https://files.catbox.moe/31m5me.mp4"
FALLBACK_NINEX_DEMO = "https://files.catbox.moe/73gkqy.mp4"

# Video storage file
VIDEOS_FILE = "videos.json"

# Default structure
DEFAULT_VIDEOS = {
    "bala_setup": None,
    "ninex_setup": None,
    "bala_demo": None,
    "ninex_demo": None,
}


def load_videos():
    if os.path.exists(VIDEOS_FILE):
        try:
            with open(VIDEOS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_VIDEOS.copy()
    return DEFAULT_VIDEOS.copy()


def save_videos(data):
    with open(VIDEOS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 BALA MOD", callback_data="mod_bala")],
        [InlineKeyboardButton("🔵 NINE-X MOD", callback_data="mod_ninex")],
        [InlineKeyboardButton("🎥 Watch Demo Videos", callback_data="show_demos")],
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

    try:
        if update.message:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        elif update.callback_query:
            await update.callback_query.answer()
            try:
                await update.callback_query.message.edit_text(
                    welcome_text, reply_markup=reply_markup
                )
            except Exception:
                await update.callback_query.message.reply_text(
                    welcome_text, reply_markup=reply_markup
                )
    except Exception as e:
        logger.error(f"Start error: {e}")


# --- DEMO VIDEOS ---
async def show_demos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    videos = load_videos()

    try:
        # Bala Demo
        if videos.get("bala_demo"):
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=videos["bala_demo"],
                caption="🔴 BALA-MOD Demo Video",
            )
        else:
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=FALLBACK_BALA_DEMO,
                caption="🔴 BALA-MOD Demo Video",
            )

        # NineX Demo
        if videos.get("ninex_demo"):
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=videos["ninex_demo"],
                caption="🔵 NINE-X MOD Demo Video",
            )
        else:
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=FALLBACK_NINEX_DEMO,
                caption="🔵 NINE-X MOD Demo Video",
            )

        keyboard = [
            [InlineKeyboardButton("🔴 BALA Setup & Prices", callback_data="mod_bala")],
            [InlineKeyboardButton("🔵 NINE-X Setup & Prices", callback_data="mod_ninex")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="👆 Demo videos upar hain.\n\nNeeche se Setup & Prices choose karo:",
            reply_markup=reply_markup,
        )
    except Exception as e:
        logger.error(f"Demo error: {e}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"❌ Demo error: {e}"
        )


# --- BALA MOD ---
async def mod_bala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    videos = load_videos()

    caption = (
        "Free Fire Bala Mods 👿 Full Setup 🔥 Video || Non Root Main Safe ||\n\n"
        "🚨 BALA MOD MENU — KEY AVAILABLE NOW! 🚨\n\n"
        "🎮 NON-ROOT MOD MENU\n"
        "✅ Main ID Safe\n"
        "⚡ Quick Key Delivery\n"
        "🔥 Multiple Duration Options\n\n"
        "💰 PRICE LIST\n"
        "Neeche se apna plan choose karo 👇"
    )

    keyboard = [
        [InlineKeyboardButton("🔴 1 Hour  —  ₹35", callback_data="buy_bala_1h")],
        [InlineKeyboardButton("🔴 3 Hours —  ₹80", callback_data="buy_bala_3h")],
        [InlineKeyboardButton("🔴 6 Hours — ₹140", callback_data="buy_bala_6h")],
        [InlineKeyboardButton("🔴 12 Hours — ₹240", callback_data="buy_bala_12h")],
        [InlineKeyboardButton("🔴 24 Hours — ₹380", callback_data="buy_bala_24h")],
        [InlineKeyboardButton("🔴 2 Days  — ₹650", callback_data="buy_bala_2d")],
        [InlineKeyboardButton("🔴 3 Days  — ₹800", callback_data="buy_bala_3d")],
        [InlineKeyboardButton("🔙 Back to Demos", callback_data="show_demos")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if videos.get("bala_setup"):
            # file_id se bhejo (permanent)
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=videos["bala_setup"],
                caption=caption,
                reply_markup=reply_markup,
            )
        else:
            # fallback URL
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=FALLBACK_BALA_SETUP,
                caption=caption,
                reply_markup=reply_markup,
            )
        logger.info("Bala setup sent")
    except Exception as e:
        logger.error(f"Bala error: {e}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=caption + f"\n\n⚠️ Video load nahi hua.\nError: {e}",
            reply_markup=reply_markup,
        )


# --- NINE-X MOD ---
async def mod_ninex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    videos = load_videos()

    caption = (
        "🔵 NINE-X MOD SETUP & PRICING\n\n"
        "⏱️ Duration: 10 Days\n"
        "💵 Price: ₹500\n\n"
        "Setup video dekh lo carefully, phir neeche se purchase karo."
    )

    keyboard = [
        [InlineKeyboardButton("🔵 Purchase 10-Day Key — ₹500", callback_data="buy_ninex_10d")],
        [InlineKeyboardButton("🔙 Back to Demos", callback_data="show_demos")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        if videos.get("ninex_setup"):
            await context.bot.send_video(
                chat_id=query.message.chat_id,
                video=videos["ninex_setup"],
                caption=caption,
                reply_markup=reply_markup,
            )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=caption + "\n\n⚠️ Setup video abhi set nahi hua.\nAdmin /setup_ninex use kare.",
                reply_markup=reply_markup,
            )
    except Exception as e:
        logger.error(f"NineX error: {e}")
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=caption + f"\n\n⚠️ Error: {e}",
            reply_markup=reply_markup,
        )


# --- PAYMENT FLOW ---
async def payment_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data.replace("buy_", "").upper()
    context.user_data["selected_plan"] = plan

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

    YOUR_UPI_ID = "Q691189350@ybl"
    YOUR_QR_IMAGE_LINK = "https://files.catbox.moe/goka4u.jpg"

    qr_caption = (
        f"💳 Payment Page\n\n"
        f"📦 Plan: {plan_display}\n\n"
        "1️⃣ Scan the QR code **या** नीचे दिए UPI ID पर पेमेंट करो\n\n"
        f"📌 UPI ID: `{YOUR_UPI_ID}`\n\n"
        "2️⃣ Exact amount bhejo\n"
        "3️⃣ Neeche ✅ I Have Paid dabao\n"
        "4️⃣ Payment screenshot bhejo\n\n"
        f"🎧 Support: {SUPPORT_LINK}"
    )

    keyboard = [
        [InlineKeyboardButton("✅ I Have Paid", callback_data="i_have_paid")],
        [InlineKeyboardButton("🎧 Support Team", url=SUPPORT_LINK)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=YOUR_QR_IMAGE_LINK,
            caption=qr_caption,
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=qr_caption + f"\n\n⚠️ QR error: {e}",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )


# --- I HAVE PAID ---
async def i_have_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["waiting_for_screenshot"] = True

    await query.message.reply_text(
        "📸 Payment Screenshot Required\n\n"
        "Ab is chat mein apna Payment Screenshot bhejo.\n\n"
        "Screenshot aate hi system verify karega aur key deliver ho jayegi.\n"
        "Please wait..."
    )


# --- SCREENSHOT ---
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pehle check karo kya admin video setup kar raha hai
    if context.user_data.get("waiting_for_video"):
        await handle_admin_video(update, context)
        return

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

    forward_caption = (
        f"🔔 New Payment Proof Received!\n\n"
        f"👤 User: {user.full_name}\n"
        f"🔗 Username: @{user.username or 'No Username'}\n"
        f"🆔 User ID: `{user.id}`\n"
        f"📦 Plan: {plan_display}\n\n"
        f"Key bhejne ke liye:\n"
        f"`/sendkey {user.id} YOUR_KEY_HERE`"
    )

    try:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=forward_caption,
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Admin forward error: {e}")

    context.user_data["waiting_for_screenshot"] = False

    await update.message.reply_text(
        "✅ Screenshot successfully received!\n\n"
        "⏳ Please wait...\n"
        "Aapka key jald hi is bot mein deliver ho jayega.\n\n"
        "Admin verify karke key bhej dega.\n"
        "Dhanyavaad! 🙏"
    )


# --- ADMIN: VIDEO SETUP COMMANDS ---
async def setup_bala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "bala_setup"
    await update.message.reply_text(
        "📤 Ab **Bala Setup Video** bhejo.\n\n"
        "Video bhejne ke baad ye permanent save ho jayega.",
        parse_mode="Markdown"
    )


async def setup_ninex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "ninex_setup"
    await update.message.reply_text(
        "📤 Ab **Nine-X Setup Video** bhejo.\n\n"
        "Video bhejne ke baad ye permanent save ho jayega.",
        parse_mode="Markdown"
    )


async def setup_bala_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "bala_demo"
    await update.message.reply_text(
        "📤 Ab **Bala Demo Video** bhejo.\n\n"
        "Video bhejne ke baad ye permanent save ho jayega.",
        parse_mode="Markdown"
    )


async def setup_ninex_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "ninex_demo"
    await update.message.reply_text(
        "📤 Ab **Nine-X Demo Video** bhejo.\n\n"
        "Video bhejne ke baad ye permanent save ho jayega.",
        parse_mode="Markdown"
    )


async def handle_admin_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    video_type = context.user_data.get("waiting_for_video")
    if not video_type:
        return

    if not update.message.video and not update.message.document:
        await update.message.reply_text("❌ Sirf Video bhejo.")
        return

    # Video ya document se file_id lo
    if update.message.video:
        file_id = update.message.video.file_id
    else:
        file_id = update.message.document.file_id

    videos = load_videos()
    videos[video_type] = file_id
    save_videos(videos)

    context.user_data["waiting_for_video"] = None

    names = {
        "bala_setup": "Bala Setup Video",
        "ninex_setup": "Nine-X Setup Video",
        "bala_demo": "Bala Demo Video",
        "ninex_demo": "Nine-X Demo Video",
    }

    await update.message.reply_text(
        f"✅ {names.get(video_type, video_type)} **permanent save** ho gaya!\n\n"
        f"Ab users ko ye video dikhega.",
        parse_mode="Markdown"
    )


# --- ADMIN SEND KEY ---
async def send_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized.")
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
        await update.message.reply_text(f"✅ Key sent to User ID: {target_user_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed: {e}")


# --- VIDEO HANDLER (for admin setup) ---
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_video"):
        await handle_admin_video(update, context)


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

    # Admin setup commands
    application.add_handler(CommandHandler("setup_bala", setup_bala))
    application.add_handler(CommandHandler("setup_ninex", setup_ninex))
    application.add_handler(CommandHandler("setup_bala_demo", setup_bala_demo))
    application.add_handler(CommandHandler("setup_ninex_demo", setup_ninex_demo))

    application.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    application.add_handler(CallbackQueryHandler(show_demos, pattern="^show_demos$"))
    application.add_handler(CallbackQueryHandler(mod_bala, pattern="^mod_bala$"))
    application.add_handler(CallbackQueryHandler(mod_ninex, pattern="^mod_ninex$"))
    application.add_handler(CallbackQueryHandler(payment_flow, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(i_have_paid, pattern="^i_have_paid$"))

    # Photo for payment screenshot + Video for admin setup
    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))
    application.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

    logger.info("Bot started...")
    application.run_polling()


if __name__ == "__main__":
    main()
