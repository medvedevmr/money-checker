import logging
import microservices
import csv_writer
import stats_visualization
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ( Application, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters,)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CURRENCY_PAID, CURRENCY_DEPOSIT, CURRENCY_BALANCE, PAID, DEPOSIT, STATS, CATEGORY = range(7)

current_list = ['Paid', 100.0, 'USD', 100, 'Food', 'Max', 1000, ['01','01','2023']]

balance = [1000]

rate = [0]

personal_token = microservices.get_token()

privacy_list = microservices.get_privacy_list()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id in privacy_list:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, {}! Let's count!".format(update.message.from_user.first_name))
    else:
        return ConversationHandler.END


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id in privacy_list:
        file_name = stats_visualization.stats_pic()
        await context.bot.send_document (chat_id=update.effective_chat.id, document=open(file_name, 'rb'), filename=file_name)
    else:
        return ConversationHandler.END
    
"""PAID PART"""
async def start_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id in privacy_list:
        reply_keyboard = [["USD", "EUR", "RUB", "RSD"]]
        current_list[0] = 'Paid'
        await update.message.reply_text(
            "In what currency did you spend money?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Which currency?"
            ),
        )
        return CURRENCY_PAID
    else:
        return ConversationHandler.END

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
    rate[0] = microservices.get_rate(current_list[2])
    current_list[3] = round(float(user.text)/rate[0],2)
    balance[0] -= (current_list[1]/rate[0])
    current_list[6] = balance[0]
    current_list[7] = microservices.get_date()
    reply_keyboard = [["Groceries","Shopping","Delivery","Restaurants"],["Hobby","Cosmetics","Withdrawals","Others"]]
    await update.message.reply_text(
        "Which category?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Which category?"
        ),
    )
    return CATEGORY

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message
    current_list[4] = user.text
    current_list[5] = user.from_user.first_name
    csv_writer.add_cache(current_list)
    await update.message.reply_text("Counted! {} {} is avaliable on your account".format(round(balance[0]*rate[0],2),current_list[2]))
    return ConversationHandler.END

"""DEPOSIT PART"""

async def start_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id in privacy_list:
        reply_keyboard = [["USD", "EUR", "RUB", "RSD"]]
        current_list[0] = 'Deposit'
        await update.message.reply_text(
            "Which currency did you make deposit?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Which currency?"
            ),
        )
        return CURRENCY_DEPOSIT
    else:
        return ConversationHandler.END

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
    rate[0] = microservices.get_rate(current_list[2])
    current_list[3] = round(float(user.text)/rate[0],2)
    balance[0] += (current_list[1]/rate[0])
    current_list[4] = 'Deposit'
    current_list[5] = user.from_user.first_name
    current_list[6] = balance[0]
    current_list[7] = microservices.get_date()
    csv_writer.add_cache(current_list)
    await update.message.reply_text("Counted! {} {} is avaliable on your account".format(round(balance[0]*rate[0],2),current_list[2]))
    return ConversationHandler.END

"""Check Balance"""
async def start_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id in privacy_list:
        reply_keyboard = [["USD", "EUR", "RUB", "RSD"]]
        await update.message.reply_text(
            "Which currency do you prefer?",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Which currency?"
            ),
        )
        return CURRENCY_BALANCE
    else:
        return ConversationHandler.END

async def balance_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.text
    rate[0] = microservices.get_rate(user)
    await update.message.reply_text("Your current balance {} {}".format(round(balance[0]*rate[0],2),user))
    return ConversationHandler.END
    
"""Cancels and ends the conversation."""
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = str(update.message.from_user.id)
    if user_id in privacy_list:
        user = update.message.from_user
        await update.message.reply_text(
            "Operation Cancelled", reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END
    else:
        return ConversationHandler.END

if __name__ == '__main__':
    #exhange_rates = microservices.request_rate()
    
    application = ApplicationBuilder().token(personal_token).build()
    
    start_handler = CommandHandler('start',start)
    application.add_handler(start_handler)
    
    stats_handler = CommandHandler('stats',stats)
    application.add_handler(stats_handler)
    
    conv_handler_paid = ConversationHandler(
        entry_points=[CommandHandler('paid',start_paid)],
        states={
            CURRENCY_PAID: [MessageHandler(filters.Regex("^(USD|EUR|RUB|RSD)$"), currency_paid)],
            PAID: [MessageHandler(filters.TEXT,paid)],
            CATEGORY: [MessageHandler(filters.Regex("^(Groceries|Shopping|Delivery|Restaurants|Hobby|Cosmetics|Withdrawals|Others)$"), category)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_paid)
    
    conv_handler_deposit = ConversationHandler(
        entry_points=[CommandHandler('deposit',start_deposit)],
        states={
            CURRENCY_DEPOSIT: [MessageHandler(filters.Regex("^(USD|EUR|RUB|RSD)$"), currency_deposit)],
            DEPOSIT: [MessageHandler(filters.TEXT,deposit)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_deposit)
    
    conv_handler_balance = ConversationHandler(
        entry_points=[CommandHandler('balance',start_balance)],
        states={
            CURRENCY_BALANCE: [MessageHandler(filters.Regex("^(USD|EUR|RUB|RSD)$"), balance_check)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler_balance)
    
    application.run_polling()