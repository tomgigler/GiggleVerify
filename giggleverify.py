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
import gigsession

client = discord.Client()

async def init_user_verification(msg):
    if not gigdb.get_staff_channel_id(msg.guild.id):
        raise gigutil.GigException(f"{client.user.mention} has not been configured on this server")
    gigsession.Session(msg.author.id, msg.author.name, msg.guild.id)
    await client.get_user(msg.author.id).send(f"Welcome to the {msg.guild.name} verification process.  Type `verify` to begin")

async def process_dm(msg):
    if msg.author.id in gigsession.sessions:
        # cs is CurentSession
        cs = gigsession.sessions[msg.author.id]

        if cs.current_question == 0:
            if re.match(r'\S*verify\S*$', msg.content):
                cs.current_question = 1
                if len(cs.questions):
                    await msg.channel.send(f"Please answer the following Questions:\n\n{cs.questions[1].question}")
                    cs.save()
                else:
                    await msg.channel.send("Thank you for taking part in the verification process")
                    cs.delete()
        else:
            if cs.questions[cs.current_question].question_type == gigquestions.QuestionType.YESNO:
                if not re.match(r'\s*(yes|no)\s*', msg.content, re.IGNORECASE):
                    await msg.channel.send(f"Please answer `yes` or `no`\n{cs.questions[cs.current_question].question}")
                    return

            if cs.questions[cs.current_question].question_type == gigquestions.QuestionType.NUMBER:
                if not re.match(r'\d+', msg.content):
                    await msg.channel.send(f"This question requires a numerical answer\n{cs.questions[cs.current_question].question}")
                    return

            cs.questions[cs.current_question].response = msg.content
            cs.current_question += 1
            if cs.current_question <= len(cs.questions):
                cs.save()
                await msg.channel.send(cs.questions[cs.current_question].question)
            else:
                output = "Thank you for taking part in the verification process\n"
                await msg.channel.send(output)
                output = f"{msg.author.mention} has completed the verification process:\n\n"
                for q in cs.questions.values():
                    output += f"{q.question_num}:  {q.response}\n"
                guild = client.get_guild(cs.guild_id)
                channel = discord.utils.get(guild.channels, id=gigdb.get_staff_channel_id(cs.guild_id))
                await channel.send(output)
                cs.delete()

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

        match = re.match(r'&g(iggle)? +adduser +(\S+)( +(\S+))? *$', msg.content)
        if match and msg.author.id == bot_owner_id:
            if match.group(3):
                guild_id = int(match.group(3))
            else:
                guild_id = msg.guild.id
            giguser.save_user(int(match.group(2)), client.get_user(int(match.group(2))).name, int(guild_id))
            await msg.channel.send(f"Permissions granted for {client.get_user(int(match.group(2))).mention} in {client.get_guild(guild_id).name}")
            return

    except gigutil.GigException as e:
        try:
            await msg.channel.send(embed=discord.Embed(description=str(e), color=0xff0000))
        except:
            await giglog.log(client, f"{format_exc()}")

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
gigsession.load_sessions()
client.run(bot_token)
