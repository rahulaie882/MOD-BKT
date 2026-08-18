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

# Configurations & Credentials (Sandbox Test Mode)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8892594189:AAE6ikOmt4WU65yCBXBNvzvtKzrixDngl2I")
CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID", "TEST1114142028b99b2c8e9cff86")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY", "cfsk_ma_test_...") # Apni sandbox secret key yahan daalein
CASHFREE_ENV = "TEST"

def create_cashfree_order(amount, plan, user_id):
    """Cashfree Sandbox Orders API"""
    base = "https://sandbox.cashfree.com/pg"
    order_id = f"order_{user_id}_{uuid.uuid4().hex[:8]}"

    payload = {
        "order_id": order_id,
        "order_amount": float(amount),
        "order_currency": "INR",
        "customer_details": {
            "customer_id": f"cust_{user_id}",
            "customer_phone": "9999999999",
            "customer_email": f"user{user_id}@telegram.bot",
            "customer_name": "Test User"
        },
        "order_meta": {
            "return_url": "https://t.me/KeyShop_bot"
        },
        "order_note": f"{plan} - Telegram Bot Test"
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
        
        logger.info(f"Sandbox Response: {r.status_code} {data}")

        if r.status_code in (200, 201):
            session_id = data.get("payment_session_id")
            if session_id:
                # Sandbox Checkout Link
                payment_url = f"https://sandbox.cashfree.com/pg/orders/{order_id}/pay"
                return {
                    "success": True,
                    "order_id": order_id,
                    "payment_url": payment_url,
                }
                
        logger.error(f"Sandbox create order error: {r.status_code} {data}")
        return {"success": False, "error": data}
    except Exception as e:
        logger.error(f"Sandbox exception: {e}")
        return {"success": False, "error": str(e)}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🛒 Buy Plan (₹240) [TEST]", callback_data="buy_BALA_1H")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Hello {user.first_name}!\nWelcome to Key-Shop Bot (Sandbox Mode) 🔑\nChoose your plan below:",
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
        
        await query.message.reply_text("⏳ Test payment link ban raha hai...")
        
        result = create_cashfree_order(amount, plan, user_id)
        
        if result["success"]:
            link_url = result["payment_url"]
            kb = [[InlineKeyboardButton("💳 Pay Test Amount", url=link_url)]]
            await query.message.reply_text(
                f"✅ **Test Payment Link Created!**\n\nPlan: {plan}\nAmount: ₹{amount}",
                reply_markup=InlineKeyboardMarkup(kb),
                parse_mode="Markdown"
            )
        else:
            err_msg = str(result.get("error"))
            await query.message.reply_text(
                f"❌ Link nahi ban paya.\n\nError: `{err_msg}`",
                parse_mode="Markdown"
            )
            
    elif data == "main_menu":
        keyboard = [[InlineKeyboardButton("🛒 Buy Plan (₹240) [TEST]", callback_data="buy_BALA_1H")]]
        await query.message.edit_text("🏠 Main Menu:", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Bot started in Sandbox Mode...")
    application.run_polling()

if __name__ == "__main__":
    main()
    
