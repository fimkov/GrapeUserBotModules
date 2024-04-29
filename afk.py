import datetime
from pyrogram import Client, filters
from api import grapeapi
from api import command, modules_actions, module

afk_data = {
    "isAfk": False,
    "reason": None,
    "start_time": None
}

isAfk = filters.create(lambda _, __, ___: afk_data["isAfk"])


@Client.on_message(filters.command("afk", grapeapi.prefix.get_prefix()) & filters.me)
async def afk_command(_, message):
    try:
        reason = " ".join(message.command[1:])
    except:
        await message.edit("invalid arguments")
        return

    afk_data["reason"] = reason
    afk_data["isAfk"] = True
    afk_data["start_time"] = datetime.datetime.now().replace(microsecond=0)
    await message.edit("You have activated AFK mode")


@Client.on_message(filters.command("unafk", grapeapi.prefix.get_prefix()) & filters.me)
async def unafk(_, message):
    if not afk_data["isAfk"]:
        await message.edit("You have not activated AFK mode")
        return

    afk_data["isAfk"] = False
    afk_data["reason"] = None
    afk_data["start_time"] = None
    await message.edit("Afk mode have been disabled")


@Client.on_message(isAfk & ~filters.me & ((filters.private & ~filters.bot) | (filters.mentioned & filters.group)))
async def afk_autoaws(client, message):
    me = await client.get_me()
    await message.reply("""
❗ {} in afk
❓ reason: {}
⏲️ time in afk: {}
    """.format(me.mention(), afk_data["reason"], datetime.datetime.now().replace(microsecond=0) - afk_data["start_time"]))


afk_module = module("afk", "afk autoanswer", str(__file__), 1.0, [
    command("afk [reason]", "join to afk mode"),
    command("unafk", "disable afk mode")
])

modules_actions.add_module(afk_module)
