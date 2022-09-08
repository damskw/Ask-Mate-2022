import csv
import os

QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'questions.csv'
ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answers.csv'

def get_questions() -> list:
    with open(QUESTIONS_FILE_PATH, "r", encoding='utf-8') as file:
        questions = list(csv.DictReader(file))
        print(questions)
    return questions


def get_answers() -> list:
    with open(ANSWERS_FILE_PATH, "r", encoding='utf-8') as file:
        answers = list(csv.DictReader(file))
    return answers


def find_an_answer(question_id):
    answers = get_answers()
    all_desired_answers = []
    for answer in answers:
        if answer["question id"] == question_id:
            all_desired_answers.append(answer)
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
    with open(QUESTIONS_FILE_PATH, "a", encoding='utf-8') as file:
        file.write("\n"
                   f"{question['id']},"
                   f"{question['submission time']},"
                   f"{question['view number']},"
                   f"{question['vote number']},"
                   f"{question['title']},"
                   f"{question['message']},"
                   f"{question['image']}")


def save_answer(answer):
    with open(ANSWERS_FILE_PATH, "a", encoding='utf-8') as file:
        file.write("\n"
                   f"{answer['id']},"
                   f"{answer['submission time']},"
                   f"{answer['vote number']},"
                   f"{answer['question id']},"
                   f"{answer['message']},"
                   f"{answer['image']}")


def update_answers(answers):
    with open(ANSWERS_FILE_PATH, "w", encoding='utf-8') as file:
        file.write("id,submission time,vote number,question id,message,image\n")
        for answer in answers:
            answer['message'] = '"' + answer['message'] + '"'
            answer['image'] = '"' + answer['image'] + '"'
            file.write(f"{answer['id']},"
                       f"{answer['submission time']},"
                       f"{answer['vote number']},"
                       f"{answer['question id']},"
                       f"{answer['message']},"
                       f"{answer['image']}\n")


def update_questions(questions):
    with open(QUESTIONS_FILE_PATH, "w", encoding='utf-8') as file:
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


def edit_question(new_question):
    questions = get_questions()
    with open(QUESTIONS_FILE_PATH, "w", encoding='utf-8') as file:
        file.write("id,submission time,view number,vote number,title,message,image\n")
        for question in questions:
            if new_question['id'] == question['id']:
                if new_question.get('title'):
                    new_title = new_question['title']
                    if len(new_title) >= 10:
                        question['title'] = new_title
                question['message'] = new_question['message']
                question['image'] = new_question['image']
            question['message'] = '"' + question['message'] + '"'
            question['title'] = '"' + question['title'] + '"'
            question['image'] = '"' + question['image'] + '"'
            file.write(f"{question['id']},"
                       f"{question['submission time']},"
                       f"{question['view number']},"
                       f"{question['vote number']},"
                       f"{question['title']},"
                       f"{question['message']},"
                       f"{question['image']}\n")


def change_question_vote(question_id, direction) -> None:
    questions = get_questions()
    with open(QUESTIONS_FILE_PATH, "w", encoding='utf-8') as file:
        file.write("id,submission time,view number,vote number,title,message,image\n")
        for question in questions:
            if question['id'] == question_id:
                vote_number = int(question['vote number'])
                if direction == "UP":
                    question['vote number'] = vote_number + 1
                elif direction == "DOWN":
                    question['vote number'] = vote_number - 1
            question['message'] = '"' + question['message'] + '"'
            question['title'] = '"' + question['title'] + '"'
            question['image'] = '"' + question['image'] + '"'
            file.write(f"{question['id']},"
                       f"{question['submission time']},"
                       f"{question['view number']},"
                       f"{question['vote number']},"
                       f"{question['title']},"
                       f"{question['message']},"
                       f"{question['image']}\n")
    return None

def higher_question_view_number(question_id):
    questions = get_questions()
    with open(QUESTIONS_FILE_PATH, "w", encoding='utf-8') as file:
        file.write("id,submission time,view number,vote number,title,message,image\n")
        for question in questions:
            if question['id'] == question_id:
                view_number = int(question['view number']) + 1
                question['view number'] = view_number
            question['message'] = '"' + question['message'] + '"'
            question['title'] = '"' + question['title'] + '"'
            question['image'] = '"' + question['image'] + '"'
            file.write(f"{question['id']},"
                       f"{question['submission time']},"
                       f"{question['view number']},"
                       f"{question['vote number']},"
                       f"{question['title']},"
                       f"{question['message']},"
                       f"{question['image']}\n")
def change_answer_vote(answer_id, direction):
    answers = get_answers()
    with open(ANSWERS_FILE_PATH, "w", encoding='utf-8') as file:
        file.write("id,submission time,vote number,question id,message,image\n")
        for answer in answers:
            if answer['id'] == answer_id:
                vote_number = int(answer['vote number'])
                if direction == "UP":
                    answer['vote number'] = vote_number + 1
                elif direction == "DOWN":
                    answer['vote number'] = vote_number - 1
            answer['message'] = '"' + answer['message'] + '"'
            answer['image'] = '"' + answer['image'] + '"'
            file.write(f"{answer['id']},"
                       f"{answer['submission time']},"
                       f"{answer['vote number']},"
                       f"{answer['question id']},"
                       f"{answer['message']},"
                       f"{answer['image']}\n")
    return None


def convert_line_brakes_to_br(text):
    return "\n".join(text.split("<br>"))
