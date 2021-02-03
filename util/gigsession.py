#!/usr/bin/env python
import gigdb

sessions = {}

class SessionQuestion:
    def __init__(self, user_id, question_num, question, question_type, response=None):
        self.user_id = user_id
        self.question_num = question_num
        self.question = question
        self.question_type = question_type
        self.response = response

class Session:
    def __init__(self, user_id, user_name, guild_id, current_question=0, new=True):
        self.user_id = user_id
        self.user_name = user_name
        self.guild_id = guild_id
        self.current_question = current_question
        if new:
            self.questions = {}
            for question in gigdb.get_questions(self.guild_id):
                self.questions[question[0]] = SessionQuestion(self.user_id, question[0], question[1], question[2])
            self.save()
        else:
            self.questions = {}
            for question in gigdb.get_session_questions(self.user_id):
                self.questions[question[0]] = SessionQuestion(self.user_id, question[0], question[1], question[2], question[3])

        sessions[self.user_id] = self

    def save(self):
        gigdb.save_session(self.user_id, self.user_name, self.guild_id, self.current_question)
        for q in self.questions.values():
            gigdb.save_session_question(self.user_id, q.question_num, q.question, q.question_type, q.response)

    def delete(self):
        gigdb.delete_session(self.user_id)

def load_sessions():
    for s in gigdb.get_all("sessions"):
        Session(s[0], s[1], s[2], s[3], False)
