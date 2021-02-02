#!/usr/bin/env python
import gigdb

users = {}
user_guilds = {}

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def load_users():
    for user in gigdb.get_all("users"):
        users[user[0]] = User(user[0], user[1])
        user_guilds[user[0]] = []

    for row in gigdb.get_all("user_guilds"):
        user_guilds[row[0]].append(row[1])

def save_user(user_id, name, guild_id, guild_name):
    gigdb.save_user(user_id, name)

    gigdb.save_user_guild(user_id, guild_id, guild_name)

    if user_id not in users.keys():
        users[user_id] = User(user_id, name)

    if user_id in user_guilds.keys():
        user_guilds[user_id].append(guild_id)
    else:
        user_guilds[user_id] = [ guild_id ]
