import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'questions.csv'


def get_questions():
    questions = []
    with open(DATA_FILE_PATH, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            data = dict(line)
            questions.append(data)
    return questions


def find_a_question(id):
    questions = get_questions()
    desired_question = {}
    for question in questions:
        if question["id"] == id:
            desired_question = question
    return desired_question


def convert_line_brakes_to_br(text):
    return "\n".join(text.split("<br>"))
