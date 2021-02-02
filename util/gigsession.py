#!/usr/bin/env python
import gigdb

sessions = {}

class SessionQuestion:
    def __init__(self, user_id, question_num, question, response=None):
        self.user_id = user_id
        self.question_num = question_num
        self.question = question
        self.response = response

class Session:
    def __init__(self, user_id, user_name, guild_id):
        self.user_id = user_id
        self.user_name = user_name
        self.guild_id = guild_id
        self.current_question = 0
