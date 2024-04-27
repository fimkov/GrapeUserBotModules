from pyrogram import Client, filters
from api import grapeapi
from api import command, modules_actions, module


@Client.on_message(filters.command("trigger", grapeapi.prefix.get_prefix()) & filters.me)
async def anim_add(client, message):
    try:
        name = message.command[1]
    except IndexError:
        await message.edit(f"Command help: {grapeapi.prefix.get_prefix()}help triggers")
        return
    code = f"""from pyrogram import Client, filters
import asyncio
from api import grapeapi
from api import command, modules_actions, module

modules_actions_instance = modules_actions()

@Client.on_message(filters.command("{name}", grapeapi.prefix.get_prefix()) & filters.me)
async def {name}(client, message):"""

    aims = message.text.splitlines()
    i = 0
    o = 0

    for a in aims:
        if i == 0:
            pass
        else:
            b = a.split()
            if b[0] == "edit":
                if o == 0:
                    code = code + f"\n    await message.edit('{a.replace(b[0] + ' ', '')}')"
                else:
                    code = code + f"\n    await pensil.edit('{a.replace(b[0] + ' ', '')}')"
            elif b[0] == "send":
                o = 1
                code = code + f"\n    pensil = await message.reply('{a.replace(b[0] + ' ', '')}')"
            elif b[0] == "sleep":
                code = code + f"\n    await asyncio.sleep({a.replace(b[0] + ' ', '')})"
            elif b[0] == "remove":
                if o == 0:
                    code = code + f"\n    await message.delete()"
                else:
                    code = code + f"\n    await pensil.delete()"
            else:
                code = code + f"\n    await message.edit('{a}')"

        i = i + 1

    code = code + "\n"
    code = code + f"""
base_module = module("{name}", "custom trigger", str(__file__), 1.0, [
    command("{name}", "custom trigger")
])

modules_actions_instance.add_module(base_module)
    """

    f = open(f"plugins/{name}.py", "w", encoding='utf-8')
    f.write(code)
    f.close()

    await message.edit("The command has been successfully created!")
    await message.reply("<b>Rebooting the userbot...</b>")
    await grapeapi.restart(message=message)

triggers_module = module("triggers", "custom commands creator", str(__file__), 1.0, [
    command("triggers", "create custom command. more info: https://telegra.ph/Using-the-triggers-module-03-08")
])


modules_actions.add_module(triggers_module)
