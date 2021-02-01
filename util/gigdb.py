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

def get_questions(guild_id):
    return db_execute_sql(f"SELECT question_num, question, question_type FROM questions WHERE guild_id = {guild_id}", True)
