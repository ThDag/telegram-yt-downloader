import numexpr
from numpy._core import numeric
from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "7665493594:AAHRnkGGAz2ia45VzIiw7K3OTHBXwAh6FTE"


def calculator(args: list):
    pass


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is not None:
        await context.bot.send_message(
            update.effective_chat.id,
            "this is a calculator bot. run /calc <calculation> \n and replace <calculation> with a simple calculation seperated with spaces. \n *Ex*; '2 + 5 - 1'",
        )


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"User {update.effective_user.username} sent: {update.message.text}")
    if context.args:
        print(type(context.args))

        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=str(numexpr.evaluate(" ".join(context.args))),
            )

        except:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You have sent a invalid calculation",
            )

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="you haven't sent a calculation"
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start_command)
    calc_handler = CommandHandler("calc", calc_command)

    app.add_handler(start_handler)
    app.add_handler(calc_handler)

    print("polling..")
    app.run_polling()
