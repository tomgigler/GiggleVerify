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
    return db_execute_sql(f"SELECT * FROM {table}", True)

def get_questions(guild_id):
    return db_execute_sql("SELECT question_num, question, question_type FROM questions WHERE guild_id = %s", True, guild_id=guild_id)

def get_session_questions(user_id):
    return db_execute_sql("SELECT question_num, question, question_type, response FROM session_questions WHERE user_id = %s", True, user_id=user_id)

def save_user(id, name):
    db_execute_sql("INSERT INTO users ( id, name ) values ( %s, %s ) ON DUPLICATE KEY UPDATE name = %s", False, id=id, name_1=name, name_2=name)

def save_user_guild(user_id, guild_id):
    db_execute_sql("INSERT INTO user_guilds ( user_id, guild_id ) values (%s, %s) ON DUPLICATE KEY UPDATE guild_id = %s",
        False, user_id=user_id, guild_id=guild_id, guild_id_2=guild_id)

def save_session(user_id, user_name, guild_id, current_question):
    db_execute_sql("INSERT INTO sessions ( user_id, user_name, guild_id, current_question ) values (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE user_name=%s, guild_id = %s, current_question=%s",
        False, user_id=user_id, user_name=user_name, guild_id=guild_id, current_question=current_question, user_name_1=user_name, guild_id_1=guild_id, current_question_1=current_question)

def save_session_question(user_id, question_num, question, question_type, response):
    db_execute_sql("INSERT INTO session_questions ( user_id, question_num, question, question_type, response ) values (%s, %s, %s, %s, %s) "
        "ON DUPLICATE KEY UPDATE question = %s, question_type = %s, response = %s",
        False, user_id=user_id, q_num=question_num, q=question, q_type=question_type, response=response, q_1=question, q_type_1=question_type, response_1=response)

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

def delete_session(user_id):
    db_execute_sql("DELETE FROM sessions WHERE user_id = %s", False, user_id=user_id)
    db_execute_sql("DELETE FROM session_questions WHERE user_id = %s", False, user_id=user_id)
