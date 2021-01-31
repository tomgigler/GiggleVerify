#!/usr/bin/env python
import discord
from datetime import datetime
from traceback import format_exc
from local_settings import bot_token, bot_owner_id
import giglog

client = discord.Client()

@client.event
async def on_message(msg):
    try:
        if msg.author == client.user:
            return
        if isinstance(msg.channel, discord.channel.DMChannel):
            process_dm(msg)
        process_dm(msg)
    except:
        await giglog.log(client, f"{format_exc()}")

@client.event
async def on_ready():
    try:
        await client.change_presence(activity=discord.Game('with thegigler'))
    except:
        await giglog.log(client, f"{format_exc()}")

@client.event
async def on_guild_join(guild):
    try:
        user = client.get_user(bot_owner_id)
        await user.send(f"{client.user.mention} joined {guild.name}")
    except:
        await giglog.log(client, f"{format_exc()}")

client.run(bot_token)
