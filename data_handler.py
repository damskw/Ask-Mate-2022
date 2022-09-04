import csv
import os

QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'questions.csv'
ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answers.csv'


def get_questions():
    questions = []
    with open(QUESTIONS_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            data = dict(line)
            questions.append(data)
    return questions


def get_answers():
    answers = []
    with open(ANSWERS_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            data = dict(line)
            answers.append(data)
    return answers


def find_an_answer(question_id):
    answers = get_answers()
    desired_answer = {}
    all_desired_answers = []
    for answer in answers:
        if answer["question id"] == question_id:
            desired_answer = answer
            all_desired_answers.append(desired_answer)
    if len(all_desired_answers) == 0:
        all_desired_answers = ""
        return all_desired_answers
    return all_desired_answers


def find_a_question(id):
    questions = get_questions()
    desired_question = {}
    for question in questions:
        if question["id"] == id:
            desired_question = question
    return desired_question


def convert_line_brakes_to_br(text):
    return "\n".join(text.split("<br>"))
