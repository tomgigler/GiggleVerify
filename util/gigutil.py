#!/usr/bin/env python
import discord
import re

class GigException(Exception):
    pass

def get_channel_by_name_or_id(client, guild, channel_param):
    channel = discord.utils.get(guild.channels, name=channel_param)
    if not channel:
        try:
            channel = discord.utils.get(guild.channels, id=int(re.search(r'(\d+)', channel_param).group(1)))
        except:
            pass
    if not channel:
        raise GigException(f"Cannot find {channel_param} channel")

    #check channel permissions
    if not channel.permissions_for(channel.guild.get_member(client.user.id)).send_messages:
        raise GigException(f"**{client.user.mention}** does not have permission to send messages in {channel.mention}")

    return channel
