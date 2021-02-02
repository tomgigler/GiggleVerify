#!/usr/bin/env python
import local_settings
import mysql.connector

def db_connect():
    return mysql.connector.connect(
            host="localhost",
            user=local_settings.db_user,
            password=local_settings.db_password,
            database=local_settings.database,
            charset='utf8mb4'
            )

def db_execute_sql(sql, fetch, **kwargs):
    mydb = db_connect()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute(sql, tuple(kwargs.values()))

    rows = None
    if fetch:
        rows = mycursor.fetchall()

    mydb.commit()
    mycursor.close()
    mydb.disconnect()

    return rows

def get_all(table):
    return db_execute_sql("SELECT * FROM %s", True, table=table)

def get_questions(guild_id):
    return db_execute_sql("SELECT question_num, question, question_type FROM questions WHERE guild_id = %s", True, guild_id=guild_id)

def save_user(id, name):
    db_execute_sql("INSERT INTO users ( id, name ) values ( %s, %s ) ON DUPLICATE KEY UPDATE name = %s", False, id=id, name_1=name, name_2=name)

def save_user_guild(user_id, guild_id, guild_name):
    db_execute_sql("INSERT INTO user_guilds ( user_id, guild_id, guild_name ) values (%s, %s, %s) ON DUPLICATE KEY UPDATE guild_name = %s",
        False, user_id=user_id, guild_id=guild_id, guild_name_1=guild_name, guild_name_2=guild_name)

def update_guild(guild_id, guild_name, staff_channel_id=None, staff_channel_name=None):
    db_execute_sql("INSERT INTO guilds values (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = %s, staff_channel_id = %s, staff_channel_name = %s",
        False, guild_id=guild_id, guild_name=guild_name, staff_channel_id=staff_channel_id, staff_channel_name=staff_channel_name,
        guild_name_2=guild_name, staff_channel_id_2=staff_channel_id, staff_channel_name_2=staff_channel_name)

def get_staff_channel_id(guild_id):
    ret = None
    res = db_execute_sql("SELECT staff_channel_id FROM guilds WHERE id = %s", True, guil_id=guild_id)
    if len(res):
        ret = res[0][0]
    return ret
