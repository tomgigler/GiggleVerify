#!/usr/bin/env python
import discord
import re
from datetime import datetime
from traceback import format_exc
from local_settings import bot_token, bot_owner_id
import giglog
import gigquestions
import giguser
import gigutil
import gigdb

client = discord.Client()
current_question = {}
user_questions = {}
replies = {}

async def init_user_verification(msg):
    if not gigdb.get_staff_channel_id(msg.guild.id):
        raise gigutil.GigException(f"{client.user.mention} has not been configured on this server")
    current_question[msg.author.id] = 0
    user_questions[msg.author.id] = gigquestions.get_questions(msg.guild.id)
    replies[msg.author.id] = {}
    await client.get_user(msg.author.id).send(f"Welcome to the {msg.guild.name} verification process.  Type `verify` to begin")

async def process_dm(msg):
    if msg.author.id in current_question:
        questions = user_questions[msg.author.id]

        if current_question[msg.author.id] == 0:
            if re.match(r'\S*verify\S*$', msg.content):
                current_question[msg.author.id] = 1
                if current_question[msg.author.id] <= len(questions):
                    await msg.channel.send(questions[current_question[msg.author.id]].question)
                else:
                    await msg.channel.send("Thank you for taking part in the verification process")
                    current_question.pop(msg.author.id, None)
                    replies.pop(msg.author.id, None)
        else:
            if questions[current_question[msg.author.id]].question_type == gigquestions.QuestionType.YESNO:
                if not re.match(r'\s*(yes|no)\s*', msg.content, re.IGNORECASE):
                    await msg.channel.send(f"Please answer `yes` or `no`\n{questions[current_question[msg.author.id]].question}")
                    return

            if questions[current_question[msg.author.id]].question_type == gigquestions.QuestionType.NUMBER:
                if not re.match(r'\d+', msg.content):
                    await msg.channel.send(f"This question requires a numerical answer\n{questions[current_question[msg.author.id]].question}")
                    return

            replies[msg.author.id][current_question[msg.author.id]] = msg.content
            current_question[msg.author.id] += 1
            if current_question[msg.author.id] <= len(questions):
                await msg.channel.send(questions[current_question[msg.author.id]].question)
            else:
                output = "Thank you for taking part in the verification process\n"
                output += "Your replies:\n"
                for r in replies[msg.author.id]:
                    output += f"{r}: {replies[msg.author.id][r]}\n"
                await msg.channel.send(output)
                current_question.pop(msg.author.id)
                replies.pop(msg.author.id)

@client.event
async def on_message(msg):
    try:
        if msg.author == client.user:
            return

        if isinstance(msg.channel, discord.channel.DMChannel):
            match = re.match(r'(\d{18})\s*(.+)', msg.content)
            if match:
                user = client.get_user(bot_owner_id)
                await user.send(f"{msg.author.mention} ({msg.author.id}) said {msg.content}")

            await process_dm(msg)
            return

        if re.match(r'\s*&giggle\s*verify\s*$', msg.content):
            await init_user_verification(msg)
            return

        if re.match(r'\s*&giggle', msg.content):
            if msg.author.id not in giguser.user_guilds.keys() or msg.guild.id not in giguser.user_guilds[msg.author.id]: 
                await msg.channel.send(embed=discord.Embed(description=f"You do not have premission to interact with me on this server\n\nDM {client.user.mention} to request permission\n\n"
                    f"Your message _must_ begin with this server id `{msg.guild.id}`", color=0xff0000))
                return

        match = re.match(r'\s*&giggle\s*channel\s+(\S+)\s*$', msg.content)
        if match:
            channel = gigutil.get_channel_by_name_or_id(client, msg.guild, match.group(1))
            gigdb.update_guild(msg.guild.id, msg.guild.name, channel.id, channel.name)
            await msg.channel.send(f"Verification responses will be posted in {channel.mention}")
            return

        match = re.match(r'&giggle +adduser +(\S+)( +(\S+))? *$', msg.content)
        if match and msg.author.id == bot_owner_id:
            if match.group(3):
                guild_id = int(match.group(3))
            else:
                guild_id = msg.guild.id
            giguser.save_user(int(match.group(2)), client.get_user(int(match.group(2))).name, int(guild_id), client.get_guild(guild_id).name)
            await msg.channel.send(f"Permissions granted for {client.get_user(int(match.group(2))).mention} in {client.get_guild(guild_id).name}")
            return

    except gigutil.GigException as e:
        await msg.channel.send(embed=discord.Embed(description=str(e), color=0xff0000))

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
        gigdb.update_guild(guild.id, guild.name)
        user = client.get_user(bot_owner_id)
        await user.send(f"{client.user.mention} joined {guild.name}")
    except:
        await giglog.log(client, f"{format_exc()}")

giguser.load_users()
client.run(bot_token)
