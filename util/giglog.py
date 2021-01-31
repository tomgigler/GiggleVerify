#!/usr/bin/env python
import discord
from local_settings import bot_owner_id
from datetime import datetime

async def log(client, content):
    try:
        user = client.get_user(bot_owner_id)
        await user.send(f"`{content}`")
    except:
        logfile = open("giggleverify.log", "a")
        logfile.write(f"{datetime.now()}:\n")
        logfile.write(f"{content}\n")
        logfile.close()
