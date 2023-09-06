import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ( Application, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters,)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CURRENCY, PAID, DEPOSIT, STATS, CATEGORY = range(5)

current_list = ['Paid', 100.0, 'USD', 'Food', 'Max']

balance = [1000]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, {}! Let's count!".format(update.message.from_user.first_name))
    
"""PAID PART"""
async def start_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["USD", "EURO", "RUB", "RSD"]]
    current_list[0] = 'Paid'
    await update.message.reply_text(
        "Which currency do you prefer?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Which currency?"
        ),
    )
    return CURRENCY

async def currency_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message
    current_list[2] = user.text
    await update.message.reply_text(
        "How much did you spend?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PAID

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message
    current_list[1] = float(user.text)
    balance[0] -= current_list[1]
    reply_keyboard = [["Food", "Fun", "Delivery", "Others"]]
    await update.message.reply_text(
        "Which category?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Which category?"
        ),
    )
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message
    current_list[3] = user.text
    current_list[4] = user.from_user.first_name
    print(current_list)
    await update.message.reply_text("Counted! {} {} is avaliable on your account".format(balance[0],'USD'))
    return ConversationHandler.END

"""DEPOSIT PART"""

async def start_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["USD", "EURO", "RUB", "RSD"]]
    current_list[0] = 'Deposit'
    await update.message.reply_text(
        "Which currency do you make deposit?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Which currency?"
        ),
    )
    return CURRENCY

async def currency_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message
    current_list[2] = user.text
    await update.message.reply_text(
        "How much did you deposit?",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DEPOSIT

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message
    current_list[1] = float(user.text)
    balance[0] += current_list[1]
    current_list[3] = 'Deposit'
    current_list[4] = user.from_user.first_name
    print(current_list)
    await update.message.reply_text("Counted! {} {} is avaliable on your account".format(balance[0],'USD'))
    return ConversationHandler.END

"""Cancels and ends the conversation."""
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Operation Cancelled", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

"""Check Balance"""
async def balance_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your current balance {} {}".format(balance[0],'USD'))

if __name__ == '__main__':
    application = ApplicationBuilder().token('6016631535:AAGW1Dn7Datpmawi9LavDUWSVIliYP6DPDI').build()
    
    conv_handler_paid = ConversationHandler(
        entry_points=[CommandHandler('paid',start_paid)],
        states={
            CURRENCY: [MessageHandler(filters.Regex("^(USD|EURO|RUB|RSD)$"), currency_paid)],
            PAID: [MessageHandler(filters.TEXT,paid)],
            CATEGORY: [MessageHandler(filters.Regex("^(Food|Fun|Delivery|Others)$"), category)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_paid)
    
    conv_handler_deposit = ConversationHandler(
        entry_points=[CommandHandler('deposit',start_deposit)],
        states={
            CURRENCY: [MessageHandler(filters.Regex("^(USD|EURO|RUB|RSD)$"), currency_deposit)],
            DEPOSIT: [MessageHandler(filters.TEXT,deposit)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_deposit)
    
    balance_handler = CommandHandler('balance',balance_check)
    application.add_handler(balance_handler)
    
    application.run_polling()