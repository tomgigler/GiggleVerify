#!/usr/bin/env python
import discord
import re
from datetime import datetime
from traceback import format_exc
from local_settings import bot_token, bot_owner_id
import giglog
import gigquestions

client = discord.Client()
current_question = {}
user_guilds = {}
replies = {}

async def init_user_verification(msg):
    current_question[msg.author.id] = 0
    user_guilds[msg.author.id] = msg.guild.id
    replies[msg.author.id] = {}
    await client.get_user(msg.author.id).send(f"Welcome to the {msg.guild.name} verification process.  Type `verify` to begin")

async def process_dm(msg):
    if msg.author.id in current_question:
        if user_guilds[msg.author.id] not in gigquestions.questions:
            gigquestions.load_questions(user_guilds[msg.author.id])
        questions = gigquestions.questions[user_guilds[msg.author.id]]

        if current_question[msg.author.id] == 0:
            if re.match(r'\S*verify\S*$', msg.content):
                current_question[msg.author.id] = 1
                await msg.channel.send(questions[current_question[msg.author.id]].question)
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
            await process_dm(msg)
            return

        if re.match(r'\s*&\s*giggle\s*verify\s*$', msg.content):
            await init_user_verification(msg)
            return

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
