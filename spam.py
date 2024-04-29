from pyrogram import Client, filters
from api import grapeapi
from api import command, modules_actions, module
import asyncio

spam_chats = {}


@Client.on_message(filters.command("spam", grapeapi.prefix.get_prefix()) & filters.me)
async def spam(client, message):
    try:
        chat_id = message.chat.id
        time = int(message.command[1])
        count = int(message.command[2])
        messag = " ".join(message.command[3:])
    except:
        await message.edit("invalid arguments")

    if chat_id in spam_chats:
        if spam_chats[chat_id]:
            await message.edit("spam already activated")
            return

    await message.delete()

    spam_chats[chat_id] = True
    for i in range(count):
        if not spam_chats[chat_id]:
            break

        await client.send_message(chat_id, messag)
        await asyncio.sleep(time)


@Client.on_message(filters.command("stop_spam", grapeapi.prefix.get_prefix()) & filters.me)
async def stop_spam(client, message):
    if spam_chats[message.chat.id]:
        spam_chats[message.chat.id] = False
        await message.edit("spam stopped")
    else:
        await message.edit("spam already stopped")

spam_module = module("spam", "spamming to selected chat", str(__file__), 1.0, [
    command("spam [time] [count] [text]", "run spam with time and count and text"),
    command("stop_spam", "stop spamming to selected chat"),
])


modules_actions.add_module(spam_module)
