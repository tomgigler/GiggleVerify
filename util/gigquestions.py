#!/usr/bin/env python
import gigdb

class QuestionType:
    NUMBER = 1
    YESNO = 2
    TEXT = 3

class Question:
    def __init__(self, question, question_type):
        self.question = question
        self.question_type = question_type

def get_questions(guild_id):
    questions = {}
    for row in gigdb.get_questions(guild_id):
        questions[row[0]] = Question(row[1], row[2])
    return questions
