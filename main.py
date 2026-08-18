import logging
import os
import uuid
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Configurations & Credentials
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8892594189:AAE6ikOmt4WU65yCBXBNvzvtKzrixDngl2I")
CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID", "13380825349a5970b7d182559df2808331")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY", "cfsk_ma_prod_667d264070f7b779891858d3492244f1_88b73e61")
CASHFREE_ENV = os.getenv("CASHFREE_ENV", "PROD")

def get_cashfree_base():
    if CASHFREE_ENV.upper() == "PROD":
        return "https://api.cashfree.com/pg"
    return "https://sandbox.cashfree.com/pg"

def create_cashfree_order(amount, plan, user_id):
    """Cashfree Orders API ke through sahi payment link banata hai"""
    base = get_cashfree_base()
    order_id = f"order_{user_id}_{uuid.uuid4().hex[:8]}"

    payload = {
        "order_id": order_id,
        "order_amount": float(amount),
        "order_currency": "INR",
        "customer_details": {
            "customer_id": f"cust_{user_id}",
            "customer_phone": "9999999999",
            "customer_email": f"user{user_id}@telegram.bot",
            "customer_name": "Valued Customer"
        },
        "order_meta": {
            "return_url": "https://t.me/KeyShop_bot"
        },
        "order_note": f"{plan} - Telegram Bot"
    }

    headers = {
        "x-client-id": CASHFREE_APP_ID,
        "x-client-secret": CASHFREE_SECRET_KEY,
        "x-api-version": "2023-08-01",
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(f"{base}/orders", json=payload, headers=headers, timeout=20)
        data = r.json()
        
        if r.status_code in (200, 201) and "payment_session_id" in data:
            session_id = data["payment_session_id"]
            
            # Cashfree official checkout payment link using session id
            payment_url = f"https://checkout.cashfree.com/js/v3/index.html?payment_session_id={session_id}"
            
            return {
                "success": True,
                "order_id": order_id,
                "payment_url": payment_url,
            }
            
        logger.error(f"Cashfree create order error: {r.status_code} {data}")
        return {"success": False, "error": data}
    except Exception as e:
        logger.error(f"Cashfree order exception: {e}")
        return {"success": False, "error": str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🛒 Buy Plan (₹240)", callback_data="buy_BALA_1H")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Hello {user.first_name}!\nWelcome to Key-Shop Bot 🔑\nChoose your plan below:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id

    if data.startswith("buy_"):
        plan = data.split("_")[1]
        amount = 240.0
        
        await query.message.reply_text("⏳ Payment session ban raha hai, wait...")
        
        result = create_cashfree_order(amount, plan, user_id)
        
        if result["success"]:
            link_url = result["payment_url"]
            kb = [[InlineKeyboardButton("💳 Pay Now", url=link_url)]]
            await query.message.reply_text(
                f"✅ **Payment Order Created Successfully!**\n\nPlan: {plan}\nAmount: ₹{amount}",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="Markdown"
            )
        else:
            err_msg = str(result.get("error"))
            await query.message.reply_text(
                f"❌ Order nahi ban paya.\n\nError: `{err_msg}`",
                parse_mode="Markdown"
            )
            logger.error(f"Cashfree order fail\nUser: {user_id}\nPlan: {plan}\nError: {err_msg}")
            
    elif data == "main_menu":
        keyboard = [[InlineKeyboardButton("🛒 Buy Plan (₹240)", callback_data="buy_BALA_1H")]]
        await query.message.edit_text("🏠 Main Menu:", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Bot started with Cashfree Orders API...")
    application.run_polling()

if __name__ == "__main__":
    main()
    
