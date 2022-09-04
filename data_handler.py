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


def save_question(question):
    with open(QUESTIONS_FILE_PATH, "a") as file:
        file.write("\n"
                   f"{question['id']},"
                   f"{question['submission time']},"
                   f"{question['view number']},"
                   f"{question['vote number']},"
                   f"{question['title']},"
                   f"{question['message']},"
                   f"{question['image']}")


def save_answer(answer):
    with open(ANSWERS_FILE_PATH, "a") as file:
        file.write("\n"
                   f"{answer['id']},"
                   f"{answer['submission time']},"
                   f"{answer['vote number']},"
                   f"{answer['question id']},"
                   f"{answer['message']},"
                   f"{answer['image']}")


def update_answers(answers):
    with open(ANSWERS_FILE_PATH, "w") as file:
        file.write("id,submission time,vote number,question id,message,image\n")
        for answer in answers:
            answer['message'] = '"' + answer['message'] + '"'
            answer['image'] = '"' + answer['image'] + '"'
            file.write(f"{answer['id']},"
                       f"{answer['submission time']},"
                       f"{answer['vote number']},"
                       f"{answer['question id']},"
                       f"{answer['message']},"
                       f"{answer['image']}")


def update_questions(questions):
    with open(QUESTIONS_FILE_PATH, "w") as file:
        file.write("id,submission time,view number,vote number,title,message,image\n")
        for question in questions:
            question['title'] = '"' + question['title'] + '"'
            question['message'] = '"' + question['message'] + '"'
            question['image'] = '"' + question['image'] + '"'
            file.write(f"{question['id']},"
                       f"{question['submission time']},"
                       f"{question['view number']},"
                       f"{question['vote number']},"
                       f"{question['title']},"
                       f"{question['message']},"
                       f"{question['image']}\n")


def convert_line_brakes_to_br(text):
    return "\n".join(text.split("<br>"))
