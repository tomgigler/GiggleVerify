#!/usr/bin/env python
import discord
from datetime import datetime
from traceback import format_exc
from local_settings import bot_token, bot_owner_id

client = discord.Client()

async def log(content):
    try:
        user = client.get_user(bot_owner_id)
        await user.send(f"`{content}`")
    except:
        logfile = open("giggleverify.log", "a")
        logfile.write(f"{datetime.now()}:\n")
        logfile.write(f"{content}\n")
        logfile.close()

@client.event
async def on_message(msg):
    try:
        if msg.author == client.user:
            return
    except:
        await log(f"{format_exc()}")

@client.event
async def on_ready():
    try:
        await client.change_presence(activity=discord.Game('with thegigler'))
    except:
        await log(f"{format_exc()}")

@client.event
async def on_guild_join(guild):
    try:
        user = client.get_user(bot_owner_id)
        await user.send(f"{client.user.mention} joined {guild.name}")
    except:
        await log(f"{format_exc()}")

client.run(bot_token)
