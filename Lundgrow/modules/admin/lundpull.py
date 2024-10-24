import os
from os import environ, execle
import subprocess
import sys
from time import sleep
import asyncio

from pyrogram import filters
from Lundgrow import Bot as app
from ...config import DEV_ID, OWNER_ID

@app.on_message(filters.command("lundpull"))
async def git_pull_command(client, message):
    if int(message.from_user.id) not in DEV_ID  and int(message.from_user.id) not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        result = subprocess.run(
            ["git", "pull", "https://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@github.com/sungjinw04/Landburjhat.git", "main"],
            capture_output=True, text=True, check=True
        )
        if "Already up to date" in result.stdout:
            return await message.reply("Repo is already up to date")
        elif result.returncode == 0:
            await message.reply(f"Lund pull successful. Bot updated.\n\n`{result.stdout}`")
            await restart_bot(message)
        else:
            await message.reply("Lund pull failed. Please check the logs.")
    except subprocess.CalledProcessError as e:
        await message.reply(f"Git pull failed with error: {e.stderr}")

async def restart_bot(message):
    await message.reply("`Restarting... 🤯🤯`")
    args = [sys.executable, "-m", "Lundgrow"]  # Adjust this line as needed
    os.execle(sys.executable, *args, os.environ)
    sys.exit()
