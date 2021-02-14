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

client = discord.Client(intents=discord.Intents.all())

async def init_user_verification(msg):
    if not gigdb.get_staff_channel_id(msg.guild.id):
        raise gigutil.GigException(f"{client.user.mention} has not been configured on this server")
    user = client.get_user(bot_owner_id)
    await user.send(f"{msg.author.mention} ({msg.author.id}) has begun the verification process on **{msg.guild.name}**")
    gigsession.Session(msg.author.id, msg.author.name, msg.guild.id)
    await client.get_user(msg.author.id).send(f"Welcome to the {msg.guild.name} verification process.  Type `verify` to begin")

async def process_dm(msg):
    # if user is not currently in a session, forward to bot owner
    if not msg.author.id in gigsession.sessions:
        if msg.author.id != bot_owner_id:
            user = client.get_user(bot_owner_id)
            content = re.sub("\n", "\n> ", msg.content)
            await user.send(f"{msg.author.mention} ({msg.author.id}) said:\n> {content}")

    else:
        # cs is CurentSession
        cs = gigsession.sessions[msg.author.id]

        if cs.current_question == 0:
            if re.match(r'\S*verify\S*$', msg.content):
                cs.current_question = 1
                if len(cs.questions):
                    await msg.channel.send(f"Please answer the following Questions:\n\n{cs.questions[1].question}")
                    cs.save()
                else:
                    await msg.channel.send("Thank you for joining our server. A member of our staff will review your answers for membership eligibility.")
                    cs.delete()
        else:
            if len(msg.content) > 200:
                await msg.channel.send(f"Your answer must be fewer than 200 characters\n{cs.questions[cs.current_question].question}")
                return

            if cs.questions[cs.current_question].question_type == gigquestions.QuestionType.YESNO:
                if not re.match(r'\s*(yes|no)\s*$', msg.content, re.IGNORECASE):
                    await msg.channel.send(f"**Please answer `yes` or `no`**\n{cs.questions[cs.current_question].question}")
                    return

            if cs.questions[cs.current_question].question_type == gigquestions.QuestionType.NUMBER:
                if not re.match(r'\d+', msg.content):
                    await msg.channel.send(f"**This question requires a numerical answer**\n{cs.questions[cs.current_question].question}")
                    return

            cs.questions[cs.current_question].response = msg.content
            cs.current_question += 1
            if cs.current_question <= len(cs.questions):
                cs.save()
                await msg.channel.send(cs.questions[cs.current_question].question)
            else:
                output = "Thank you for joining our server. A member of our staff will review your answers for membership eligibility."
                await msg.channel.send(output)

                # Send results to staff_channel
                output = f"{msg.author.mention} has completed the verification process:\n\n"
                for q in cs.questions.values():
                    output += f"{q.question_num}:  {q.response}\n"
                guild = client.get_guild(cs.guild_id)
                channel = discord.utils.get(guild.channels, id=gigdb.get_staff_channel_id(cs.guild_id))
                await channel.send(output)

                # DM Bot owner
                user = client.get_user(bot_owner_id)
                await user.send(f"{msg.author.mention} ({msg.author.id}) has completed the verification process on **{guild.name}**\n")
                cs.delete()

                # Send confirmation to message_channel
                output = f"{msg.author.mention} has completed the DM verification questions"
                channel = discord.utils.get(guild.channels, id=gigdb.get_message_channel_id(cs.guild_id))
                await channel.send(output)

@client.event
async def on_message(msg):
    try:
        if msg.author == client.user:
            return

        if isinstance(msg.channel, discord.channel.DMChannel):
            if msg.author.id == bot_owner_id:
                match = re.match(r'(\d{18})\s*(.+)', msg.content)
                if match:
                    user = client.get_user(int(match.group(1)))
                    try:
                        await user.send(f"{match.group(2)}")
                    except:
                        await msg.channel.send(f"Failed to send to {match.group(1)}")
            await process_dm(msg)
            return

        if re.match(r'\s*&giggle\s*verify\s*$', msg.content):
            await init_user_verification(msg)
            return

        if re.match(r'\s*&giggle', msg.content):
            if msg.author.id not in giguser.user_guilds.keys() or msg.guild.id not in giguser.user_guilds[msg.author.id]: 
                await msg.channel.send(embed=discord.Embed(description=f"You do not have premission to interact with me on this server\n\nDM {client.user.mention} to request permission" , color=0xff0000))
                return

        match = re.match(r'\s*&giggle\s+members\s*$', msg.content)
        if match:
            await msg.channel.send(f"The server currently has {len(msg.guild.members)} members")
            return

        match = re.match(r'\s*&giggle\s+role\s+(.*\S+)$', msg.content)
        if match:
            role = discord.utils.get(msg.guild.roles, name=match.group(1))
            if not role:
                await msg.channel.send(f"Cannot find role **{match.group(1)}**")
            else:
                await msg.channel.send(f"{len(role.members)} members currently have the {role.name} role")
            return

        match = re.match(r'\s*&giggle\s+staff_channel\s+(\S+)\s*$', msg.content)
        if match:
            channel = gigutil.get_channel_by_name_or_id(client, msg.guild, match.group(1))
            gigdb.update_guild_staff_channel(msg.guild.id, msg.guild.name, channel.id, channel.name)
            await msg.channel.send(f"Verification responses will be posted in {channel.mention}")
            return

        match = re.match(r'\s*&giggle\s+message_channel\s+(\S+)\s*$', msg.content)
        if match:
            channel = gigutil.get_channel_by_name_or_id(client, msg.guild, match.group(1))
            gigdb.update_guild_message_channel(msg.guild.id, msg.guild.name, channel.id, channel.name)
            await msg.channel.send(f"Verification completion notices will be posted in {channel.mention}")
            return

        match = re.match(r'&g(iggle)? +adduser +(\S+)( +(\S+))? *$', msg.content)
        if match and msg.author.id == bot_owner_id:
            guild = msg.guild
            if match.group(3):
                guild = client.get_guild(int(match.group(3)))
                if not guild:
                    raise gigutil.GigException(f"Cannot find Server {match.group(3)}")
            user = client.get_user(int(match.group(2)))
            if not user:
                raise gigutil.GigException(f"Cannot find user {match.group(2)}")
            giguser.save_user(user.id, user.name, guild.id)
            await msg.channel.send(f"Permissions granted for {user.mention} in {guild.name}")
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
