# Know: if the update or context features give error "it not known of None bla bla" put it inside a if statement checking that the thing is not None

import os
from typing import Final

import numexpr
import validators
from dotenv import load_dotenv
from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from videoDownloader import deleteVideo, downloadVideo

load_dotenv()

TOKEN: Final = os.getenv("TELEGRAM_TOKEN")


keyboard_animals = [
    [InlineKeyboardButton("cat", callback_data="animal_cat")],
    [InlineKeyboardButton("dog", callback_data="animal_dog")],
    [InlineKeyboardButton("monkey", callback_data="animal_monkey")],
]


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is not None:  # to stop the Lsp warning
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Hello World!"
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
            chat_id=update.effective_chat.id, text="Please send the calculation"
        )
        return CALC_FOLLOWUP


async def calc_followup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("---calc_followup activated---")
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(numexpr.evaluate(update.message.text)),
        )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You have sent a invalid calculation",
        )
        return ConversationHandler.END


async def animal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is not None:  # to stop the Lsp warning
        reply_markup = InlineKeyboardMarkup(keyboard_animals)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Inside the options that's below this text, select a animal. the thing is, those options are a really cool feature"
            "\n\n I have a suprise for you when you choose.",
            reply_markup=reply_markup,
        )


async def animal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (
        update.callback_query is not None and update.effective_chat is not None
    ):  # to stop the Lsp warning
        query = update.callback_query
        await query.answer("you made your choice.")
        await query.edit_message_text(
            "Inside the options that's below this text, select a animal. the thing it those options are a really cool feature"
            f"\n\n you chose: {query.data}"
        )
        if query.data == "animal_cat":
            print("--cat chosen, sending pussy pic--")
            await context.bot.send_photo(
                update.effective_chat.id,
                "https://i.pinimg.com/736x/8c/13/c4/8c13c4b2e0af1edea4e7b2b7a24106ca.jpg",
                "here is the suprise",
            )
        if query.data == "animal_dog":
            print("--dog chosen, sending pussy pic--")
            await context.bot.send_photo(
                update.effective_chat.id,
                "https://i.imgflip.com/9fi9je.png",
                "here is the suprise",
            )
        if query.data == "animal_monkey":
            print("--monkey chosen, sending pussy pic--")
            await context.bot.send_photo(
                update.effective_chat.id,
                "https://i.pinimg.com/1200x/de/b5/a2/deb5a20742a17bd22d0dd9793c0c4f20.jpg",
                "here is the suprise",
            )


async def hi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None and update.effective_user is not None:
        user = update.effective_user

        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )


async def dowloader_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.args == []:
        await context.bot.send_message(
            update.effective_chat.id, "Please send the link(s)"
        )

        return DOWNLOADASKFORLINK

    else:

        context.user_data["links_to_download"] = context.args

        await context.bot.send_message(
            update.effective_chat.id,
            "Please choose the length of (each) video in seconds.",
        )

        return DOWNLOADCONTINIUM


async def download_askforlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("download askforlink activated")  # debug
    print(update.message.text.split())  # debug

    try:
        context.user_data["links_to_download"] = update.message.text.split()
    except:
        print("error when writing data to user data in download_askforlink")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="there has been a error, probably your fault because my code is flawless.",
        )

        return DOWNLOADASKFORLINK

    # validate if the urls are legit
    for i in context.user_data.get("links_to_download", []):
        if not validators.url(i):
            print(f"invalid link found in input {i}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=f"invalid link found '{i}'"
            )

            return DOWNLOADASKFORLINK

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please choose the length of (each) video in seconds.",
    )

    return DOWNLOADCONTINIUM


async def download_continium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("download continium activated")  # debug

    wait_message = await context.bot.send_message(
        update.effective_chat.id, "This may take a while (like a lot)"
    )

    print("about to run downloadvideo function")  # debug
    downloadVideo_return = downloadVideo(
        context.user_data.get("links_to_download", []), int(update.message.text)
    )
    print(downloadVideo_return, "this the the output from downloadVideo ")  # debug

    if isinstance(downloadVideo_return, str):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"There has been an error, lol sorry. \nError code if you care: \n{downloadVideo_return}",
            disable_web_page_preview=True,
        )

    else:
        await wait_message.edit_text("Done, Sending the video(s)")
        for i in downloadVideo_return:
            with open(i, "rb") as file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id, video=file, caption=i
                )
            deleteVideo(i)

    return ConversationHandler.END


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="cancelled")
    return ConversationHandler.END


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if (
        update.effective_user is not None
        and update.message is not None
        and update.effective_chat is not None
        and update.message.text is not None
    ):  # to stop the Lsp warning
        # responds with the same text
        print(
            f"message send by {update.effective_user.username}: {update.message.text}"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=update.message.text
        )


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    message_handler = MessageHandler(filters.TEXT, handle_message)
    start_handler = CommandHandler("start", start_command)
    inlinekeyboard_handler = CommandHandler("animal", animal_command)
    hi_handler = CommandHandler("hi", hi_command)
    calc_handler = CommandHandler("calc", calc_command)
    downloader_handler = CommandHandler("download", dowloader_command)
    cancel_handler = CommandHandler("cancel", cancel_command)

    CALC_FOLLOWUP = 1
    calc_convo = ConversationHandler(
        entry_points=[calc_handler],  # ignore ER
        states={CALC_FOLLOWUP: [MessageHandler(filters.TEXT, calc_followup)]},
        fallbacks=[],
    )

    DOWNLOADCONTINIUM = 1
    DOWNLOADASKFORLINK = 2
    downloader_convo = ConversationHandler(
        entry_points=[downloader_handler],
        states={
            DOWNLOADCONTINIUM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, download_continium),
            ],
            DOWNLOADASKFORLINK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, download_askforlink),
            ],
        },
        fallbacks=[cancel_handler],
    )

    callback_handler = CallbackQueryHandler(
        animal_callback, pattern="animal_*"
    )  # only for the callback queries thats callback_data starts with "animal_"

    app.add_handler(start_handler)
    app.add_handler(inlinekeyboard_handler)
    app.add_handler(hi_handler)
    app.add_handler(downloader_convo)
    app.add_handler(calc_convo)

    app.add_handler(callback_handler)

    app.add_handler(message_handler)

    print("polling..")
    app.run_polling()
