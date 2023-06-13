from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Define the price list as a dictionary
price_list = {
    'item1': 10,
    'item2': 20,
    'item3': 15,
    # Add more items with their respective prices
}

# Command handler for the /start command
def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Selling Bot!")

# Command handler for the /price command
def price(update: Update, context):
    keyboard = []
    for item in price_list:
        button = InlineKeyboardButton(text=item, callback_data=item)
        keyboard.append([button])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Select an item:", reply_markup=reply_markup)

# Callback handler for item selection
def item_selected(update: Update, context):
    query = update.callback_query
    item = query.data
    price = price_list.get(item)
    if price:
        context.bot.send_message(chat_id=query.message.chat_id, text=f"The price of {item} is ${price}")
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="Item not found.")

def main():
    # Create the Telegram Updater and dispatcher
    updater = Updater("6189733110:AAGYkJws-5OjY1RFy_INzcA4OPPFEEM3d0Q", use_context=True)
    dispatcher = updater.dispatcher

    # Register command and callback handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(CallbackQueryHandler(item_selected))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
