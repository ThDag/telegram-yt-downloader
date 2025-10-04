# main file

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


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is not None:  # to stop the Lsp warning
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hi. Use the /download command. I have nothing else going on.",
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
    downloader_handler = CommandHandler("download", dowloader_command)
    cancel_handler = CommandHandler("cancel", cancel_command)

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

    app.add_handler(start_handler)
    app.add_handler(downloader_convo)

    app.add_handler(message_handler)

    print("polling..")
    app.run_polling()
