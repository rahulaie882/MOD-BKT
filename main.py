import logging
import json
import os
import uuid
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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== CONFIG ====================
BOT_TOKEN = "8892594189:AAE6ikOmt4WU65yCBXBNvzvtKzrixDngl2I"
ADMIN_ID = 8999416691
SUPPORT_LINK = "https://t.me/VIDEO_GROUP_PURCHASE"
MOD_APK_LINK = "https://t.me/+K83iEBrWmwphNGFl"

# ---------- CASHFREE (Railway Variables se lega) ----------
# Railway me Variables add karo:
#   CASHFREE_APP_ID = tumhari_app_id
#   CASHFREE_SECRET_KEY = tumhari_secret_key
#   CASHFREE_ENV = PROD
# TEMP: direct keys (baad me Variables pe wapas chale jana)
CASHFREE_APP_ID = os.environ.get("CASHFREE_APP_ID", "13380825349a5970b7d182559df2808331")
CASHFREE_SECRET_KEY = os.environ.get("CASHFREE_SECRET_KEY", "cfsk_ma_prod_e6597b2e4dcfa30511d013ed8858d689_506cf598")
CASHFREE_ENV = os.environ.get("CASHFREE_ENV", "PROD")  # PROD = Live, TEST = Sandbox
# ----------------------------------------------------------

FALLBACK_BALA_SETUP = "https://files.catbox.moe/p1xt51.mp4"
FALLBACK_BALA_DEMO = "https://files.catbox.moe/31m5me.mp4"
FALLBACK_NINEX_DEMO = "https://files.catbox.moe/73gkqy.mp4"

VIDEOS_FILE = "videos.json"
ORDERS_FILE = "orders.json"

DEFAULT_VIDEOS = {
    "bala_setup": None,
    "ninex_setup": None,
    "bala_demo": None,
    "ninex_demo": None,
}

# Plan prices (rupees)
PLAN_PRICES = {
    "BALA_1H": 35,
    "BALA_3H": 80,
    "BALA_6H": 140,
    "BALA_12H": 240,
    "BALA_24H": 380,
    "BALA_2D": 650,
    "BALA_3D": 800,
    "NINEX_10D": 500,
}

PLAN_NAMES = {
    "BALA_1H": "Bala Mod — 1 Hour (₹35)",
    "BALA_3H": "Bala Mod — 3 Hours (₹80)",
    "BALA_6H": "Bala Mod — 6 Hours (₹140)",
    "BALA_12H": "Bala Mod — 12 Hours (₹240)",
    "BALA_24H": "Bala Mod — 24 Hours (₹380)",
    "BALA_2D": "Bala Mod — 2 Days (₹650)",
    "BALA_3D": "Bala Mod — 3 Days (₹800)",
    "NINEX_10D": "Nine-X Mod — 10 Days (₹500)",
}


def load_videos():
    if os.path.exists(VIDEOS_FILE):
        try:
            with open(VIDEOS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_VIDEOS.copy()


def save_videos(data):
    with open(VIDEOS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_orders(data):
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_cashfree_base():
    if CASHFREE_ENV.upper() == "TEST":
        return "https://sandbox.cashfree.com/pg"
    return "https://api.cashfree.com/pg"


def create_payment_link(amount, plan, user_id, user_name="Customer"):
    """Cashfree Payment Link banata hai"""
    base = get_cashfree_base()
    link_id = f"tg_{user_id}_{uuid.uuid4().hex[:8]}"

    payload = {
        "customer_details": {
            "customer_phone": "9999999999",
            "customer_email": f"user{user_id}@telegram.bot",
            "customer_name": str(user_name)[:50] or "Customer",
        },
        "link_id": link_id,
        "link_amount": float(amount),
        "link_currency": "INR",
        "link_purpose": f"{plan} - Telegram Bot",
        "link_partial_payments": False,
        "link_notes": {
            "telegram_user_id": str(user_id),
            "plan": plan,
        },
    }

    headers = {
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "x-api-version": "2025-01-01",
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(f"{base}/links", json=payload, headers=headers, timeout=20)
        data = r.json()
        if r.status_code in (200, 201) and data.get("link_url"):
            return {
                "success": True,
                "link_id": data.get("link_id") or link_id,
                "link_url": data["link_url"],
                "cf_link_id": data.get("cf_link_id"),
            }
        logger.error(f"Cashfree create link error: {r.status_code} {data}")
        return {"success": False, "error": data}
    except Exception as e:
        logger.error(f"Cashfree exception: {e}")
        return {"success": False, "error": str(e)}


def check_payment_status(link_id):
    """Payment link ka status check karta hai"""
    base = get_cashfree_base()
    headers = {
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "x-api-version": "2025-01-01",
    }
    try:
        r = requests.get(f"{base}/links/{link_id}", headers=headers, timeout=15)
        data = r.json()
        if r.status_code == 200:
            status = (data.get("link_status") or "").upper()
            amount_paid = float(data.get("link_amount_paid") or 0)
            return {
                "success": True,
                "status": status,
                "amount_paid": amount_paid,
                "paid": status == "PAID" or amount_paid > 0,
                "raw": data,
            }
        return {"success": False, "error": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ==================== HANDLERS ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔴 BALA MOD", callback_data="mod_bala", style="danger")],
        [InlineKeyboardButton("🔵 NINE-X MOD", callback_data="mod_ninex", style="primary")],
        [InlineKeyboardButton("🎥 Watch Demo Videos", callback_data="show_demos", style="primary")],
        [InlineKeyboardButton("📱 Mod APK Group", url=MOD_APK_LINK)],
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
                await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup)
            except Exception:
                await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Start error: {e}")


async def show_demos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    videos = load_videos()

    try:
        if videos.get("bala_demo"):
            await context.bot.send_video(chat_id=query.message.chat_id, video=videos["bala_demo"], caption="🔴 BALA-MOD Demo Video")
        else:
            await context.bot.send_video(chat_id=query.message.chat_id, video=FALLBACK_BALA_DEMO, caption="🔴 BALA-MOD Demo Video")

        if videos.get("ninex_demo"):
            await context.bot.send_video(chat_id=query.message.chat_id, video=videos["ninex_demo"], caption="🔵 NINE-X MOD Demo Video")
        else:
            await context.bot.send_video(chat_id=query.message.chat_id, video=FALLBACK_NINEX_DEMO, caption="🔵 NINE-X MOD Demo Video")

        keyboard = [
            [InlineKeyboardButton("🔴 BALA Setup & Prices", callback_data="mod_bala", style="danger")],
            [InlineKeyboardButton("🔵 NINE-X Setup & Prices", callback_data="mod_ninex", style="primary")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu", style="primary")],
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="👆 Demo videos upar hain.\n\nNeeche se Setup & Prices choose karo:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    except Exception as e:
        logger.error(f"Demo error: {e}")
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"❌ Demo error: {e}")


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

    try:
        video = videos.get("bala_setup") or FALLBACK_BALA_SETUP
        await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=video,
            caption=caption,
            reply_markup=reply_markup,
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=caption + f"\n\n⚠️ Video: {e}",
            reply_markup=reply_markup,
        )


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
        [InlineKeyboardButton("🔵 Purchase 10-Day Key — ₹500", callback_data="buy_ninex_10d", style="primary")],
        [InlineKeyboardButton("🔙 Back to Demos", callback_data="show_demos", style="primary")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu", style="primary")],
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
                text=caption + "\n\n⚠️ Setup video abhi set nahi hua. /setup_ninex use karo.",
                reply_markup=reply_markup,
            )
    except Exception as e:
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=caption + f"\n\n⚠️ Error: {e}",
            reply_markup=reply_markup,
        )


# ---------- CASHFREE PAYMENT FLOW ----------
async def payment_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data.replace("buy_", "").upper()
    amount = PLAN_PRICES.get(plan)
    plan_display = PLAN_NAMES.get(plan, plan)

    if not amount:
        await query.message.reply_text("❌ Invalid plan.")
        return

    user = query.from_user
    await query.message.reply_text("⏳ Payment link ban raha hai, wait...")

    result = create_payment_link(
        amount=amount,
        plan=plan,
        user_id=user.id,
        user_name=user.full_name or user.username or "Customer",
    )

    if not result.get("success"):
        err = result.get("error", "Unknown error")
        await query.message.reply_text(
            f"❌ Payment link nahi ban paya.\n\n"
            f"Error: `{err}`\n\n"
            f"Admin ko batao (Cashfree keys check karo).",
            parse_mode="Markdown",
        )
        # Admin ko bhi bata do
        try:
            await context.bot.send_message(
                ADMIN_ID,
                f"⚠️ Cashfree link fail\nUser: {user.id}\nPlan: {plan}\nError: {err}",
            )
        except Exception:
            pass
        return

    link_id = result["link_id"]
    link_url = result["link_url"]

    # Order save karo
    orders = load_orders()
    orders[link_id] = {
        "user_id": user.id,
        "plan": plan,
        "amount": amount,
        "status": "ACTIVE",
        "username": user.username,
        "name": user.full_name,
    }
    save_orders(orders)

    context.user_data["current_link_id"] = link_id
    context.user_data["selected_plan"] = plan

    keyboard = [
        [InlineKeyboardButton("💳 Pay Now", url=link_url)],
        [InlineKeyboardButton("✅ Verify Payment", callback_data=f"verify_{link_id}", style="success")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu", style="primary")],
    ]

    text = (
        f"💳 **Payment Page**\n\n"
        f"📦 Plan: {plan_display}\n"
        f"💰 Amount: ₹{amount}\n\n"
        f"1️⃣ Neeche **Pay Now** dabao\n"
        f"2️⃣ Payment complete karo\n"
        f"3️⃣ Wapas aake **✅ Verify Payment** dabao\n\n"
        f"🔗 Link: {link_url}\n\n"
        f"📱 Mod APK: {MOD_APK_LINK}"
    )

    await query.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def verify_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    link_id = query.data.replace("verify_", "")
    orders = load_orders()
    order = orders.get(link_id)

    if not order:
        await query.message.reply_text("❌ Order nahi mila. Naya payment link lo.")
        return

    if order.get("status") == "PAID":
        await query.message.reply_text("✅ Ye payment pehle hi verify ho chuka hai.")
        return

    await query.message.reply_text("🔍 Payment check kar raha hoon...")

    status_result = check_payment_status(link_id)

    if not status_result.get("success"):
        await query.message.reply_text(
            f"❌ Status check fail.\n`{status_result.get('error')}`",
            parse_mode="Markdown",
        )
        return

    if status_result.get("paid"):
        # Mark paid
        order["status"] = "PAID"
        orders[link_id] = order
        save_orders(orders)

        plan = order["plan"]
        plan_display = PLAN_NAMES.get(plan, plan)
        user_id = order["user_id"]

        # User ko success message
        await query.message.reply_text(
            f"✅ **Payment Successful!**\n\n"
            f"📦 Plan: {plan_display}\n"
            f"💰 Paid: ₹{order['amount']}\n\n"
            f"⏳ Aapka key jald deliver ho raha hai...\n"
            f"Admin verify karke key bhej dega.\n\n"
            f"📱 Mod APK Group: {MOD_APK_LINK}",
            parse_mode="Markdown",
        )

        # Admin ko notify
        try:
            await context.bot.send_message(
                ADMIN_ID,
                f"💰 **AUTO PAYMENT SUCCESS**\n\n"
                f"👤 User ID: `{user_id}`\n"
                f"🔗 @{order.get('username') or 'N/A'}\n"
                f"📛 {order.get('name')}\n"
                f"📦 Plan: {plan_display}\n"
                f"💵 Amount: ₹{order['amount']}\n"
                f"🆔 Link ID: `{link_id}`\n\n"
                f"Key bhejo:\n`/sendkey {user_id} YOUR_KEY_HERE`",
                parse_mode="Markdown",
            )
        except Exception as e:
            logger.error(f"Admin notify error: {e}")

    else:
        await query.message.reply_text(
            f"⏳ Payment abhi complete nahi hua.\n\n"
            f"Status: `{status_result.get('status')}`\n"
            f"Amount Paid: ₹{status_result.get('amount_paid', 0)}\n\n"
            f"Pehle **Pay Now** se payment karo, phir Verify dabao.",
            parse_mode="Markdown",
        )


# ---------- ADMIN VIDEO SETUP ----------
async def setup_bala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "bala_setup"
    await update.message.reply_text("📤 Ab **Bala Setup Video** bhejo.", parse_mode="Markdown")


async def setup_ninex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "ninex_setup"
    await update.message.reply_text("📤 Ab **Nine-X Setup Video** bhejo.", parse_mode="Markdown")


async def setup_bala_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "bala_demo"
    await update.message.reply_text("📤 Ab **Bala Demo Video** bhejo.", parse_mode="Markdown")


async def setup_ninex_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    context.user_data["waiting_for_video"] = "ninex_demo"
    await update.message.reply_text("📤 Ab **Nine-X Demo Video** bhejo.", parse_mode="Markdown")


async def handle_admin_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    video_type = context.user_data.get("waiting_for_video")
    if not video_type:
        return
    if not update.message.video and not update.message.document:
        await update.message.reply_text("❌ Sirf Video bhejo.")
        return

    file_id = update.message.video.file_id if update.message.video else update.message.document.file_id
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
        f"✅ {names.get(video_type, video_type)} **permanent save** ho gaya!",
        parse_mode="Markdown",
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_video"):
        await handle_admin_video(update, context)


# ---------- SEND KEY ----------
async def send_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Not authorized.")
        return
    if len(context.args) < 2:
        await update.message.reply_text(
            "⚠️ Usage:\n`/sendkey <UserID> <KEY>`",
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
        f"📱 Mod APK Group: {MOD_APK_LINK}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "JIBON MODS SHOP • Premium Quality"
    )

    try:
        await context.bot.send_message(chat_id=target_user_id, text=bill_message, parse_mode="Markdown")
        await update.message.reply_text(f"✅ Key sent to {target_user_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ Failed: {e}")


def main():
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .read_timeout(60)
        .write_timeout(60)
        .connect_timeout(60)
        .pool_timeout(60)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendkey", send_key))
    app.add_handler(CommandHandler("setup_bala", setup_bala))
    app.add_handler(CommandHandler("setup_ninex", setup_ninex))
    app.add_handler(CommandHandler("setup_bala_demo", setup_bala_demo))
    app.add_handler(CommandHandler("setup_ninex_demo", setup_ninex_demo))

    app.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(show_demos, pattern="^show_demos$"))
    app.add_handler(CallbackQueryHandler(mod_bala, pattern="^mod_bala$"))
    app.add_handler(CallbackQueryHandler(mod_ninex, pattern="^mod_ninex$"))
    app.add_handler(CallbackQueryHandler(payment_flow, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(verify_payment, pattern="^verify_"))

    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

    logger.info("Bot started with Cashfree...")
    app.run_polling()


if __name__ == "__main__":
    main()
