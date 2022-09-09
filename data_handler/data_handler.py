import csv
import os
import config
from utils import quote

QUESTIONS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'questions.csv'
ANSWERS_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'answers.csv'


def get_questions() -> list:
    with open(QUESTIONS_FILE_PATH, config.READ, encoding=config.UTF_8) as file:
        questions = list(csv.DictReader(file))
    return questions


def get_answer(answer_id) -> dict or None:
    try:
        answer = next(filter(lambda item: item[config.ID] == answer_id, get_answers()))
    except StopIteration:
        return None
    return answer


def get_answers() -> list:
    with open(ANSWERS_FILE_PATH, config.READ, encoding=config.UTF_8) as file:
        answers = list(csv.DictReader(file))
    return answers


def get_answers_to_question(question_id) -> list or None:
    answers = get_answers()
    answers_to_question = []
    for answer in answers:
        if answer[config.QUESTION_ID] == question_id:
            answers_to_question.append(answer)
    # answers_to_question = filter(lambda answer: answer[config.QUESTION_ID] == question_id, answers)
    # if len(answers_to_question) == 0:
    #     return None
    return answers_to_question


def get_question(question_id) -> dict or None:
    questions = get_questions()
    try:
        desired_question = next(filter(lambda question: question[config.ID] == question_id, questions))
    except StopIteration:
        return None
    return desired_question


def save_question(question):
    with open(QUESTIONS_FILE_PATH, config.APPEND, encoding=config.UTF_8) as file:
        file.write("\n"
                   f"{question[config.ID]},"
                   f"{question[config.SUBMISSION_TIME]},"
                   f"{question[config.VIEW_NUMBER]},"
                   f"{question[config.VOTE_NUMBER]},"
                   f"{question[config.TITLE]},"
                   f"{question[config.MESSAGE]},"
                   f"{question[config.IMAGE]}")


def save_answer(answer):
    with open(ANSWERS_FILE_PATH, config.APPEND, encoding=config.UTF_8) as file:
        file.write("\n"
                   f"{answer[config.ID]},"
                   f"{answer[config.SUBMISSION_TIME]},"
                   f"{answer[config.VOTE_NUMBER]},"
                   f"{answer[config.QUESTION_ID]},"
                   f"{answer[config.MESSAGE]},"
                   f"{answer[config.IMAGE]}")


def update_answers(answers):
    with open(ANSWERS_FILE_PATH, config.WRITE, encoding=config.UTF_8) as file:
        file.write(config.ANSWER_HEADER)
        for answer in answers:
            answer[config.MESSAGE] = quote(answer[config.MESSAGE])
            answer[config.IMAGE] = quote(answer[config.IMAGE])
            file.write(f"{answer[config.ID]},"
                       f"{answer[config.SUBMISSION_TIME]},"
                       f"{answer[config.VOTE_NUMBER]},"
                       f"{answer[config.QUESTION_ID]},"
                       f"{answer[config.MESSAGE]},"
                       f"{answer[config.IMAGE]}\n")


def update_questions(questions):
    with open(QUESTIONS_FILE_PATH, config.WRITE, encoding=config.UTF_8) as file:
        file.write(config.QUESTION_HEADER)
        for question in questions:
            question[config.TITLE] = quote(question[config.TITLE])
            question[config.MESSAGE] = quote(question[config.MESSAGE])
            question[config.IMAGE] = quote(question[config.IMAGE])
            file.write(f"{question[config.ID]},"
                       f"{question[config.SUBMISSION_TIME]},"
                       f"{question[config.VIEW_NUMBER]},"
                       f"{question[config.VOTE_NUMBER]},"
                       f"{question[config.TITLE]},"
                       f"{question[config.MESSAGE]},"
                       f"{question[config.IMAGE]}\n")


def edit_question(new_question) -> bool:
    questions = get_questions()
    with open(QUESTIONS_FILE_PATH, config.WRITE, encoding=config.UTF_8) as file:
        file.write(config.QUESTION_HEADER)
        for question in questions:
            if new_question[config.ID] == question[config.ID]:
                if new_question.get(config.TITLE):
                    new_title = new_question[config.TITLE]
                    if len(new_title) >= 10:
                        question[config.TITLE] = new_title
                question[config.MESSAGE] = new_question[config.MESSAGE]
                question[config.IMAGE] = new_question[config.IMAGE]
            question[config.MESSAGE] = quote(question[config.MESSAGE])
            question[config.TITLE] = quote(question[config.TITLE])
            question[config.IMAGE] = quote(question[config.IMAGE])
            file.write(f"{question[config.ID]},"
                       f"{question[config.SUBMISSION_TIME]},"
                       f"{question[config.VIEW_NUMBER]},"
                       f"{question[config.VOTE_NUMBER]},"
                       f"{question[config.TITLE]},"
                       f"{question[config.MESSAGE]},"
                       f"{question[config.IMAGE]}\n")
    return True


def change_question_vote(question_id, direction) -> None:
    questions = get_questions()
    with open(QUESTIONS_FILE_PATH, config.WRITE, encoding=config.UTF_8) as file:
        file.write(config.QUESTION_HEADER)
        for question in questions:
            if question[config.ID] == question_id:
                vote_number = int(question[config.VOTE_NUMBER])
                if direction == config.UP:
                    question[config.VOTE_NUMBER] = vote_number + 1
                elif direction == config.DOWN:
                    question[config.VOTE_NUMBER] = vote_number - 1
            question[config.MESSAGE] = quote(question[config.MESSAGE])
            question[config.TITLE] = quote(question[config.TITLE])
            question[config.IMAGE] = quote(question[config.IMAGE])
            file.write(f"{question[config.ID]},"
                       f"{question[config.SUBMISSION_TIME]},"
                       f"{question[config.VIEW_NUMBER]},"
                       f"{question[config.VOTE_NUMBER]},"
                       f"{question[config.TITLE]},"
                       f"{question[config.MESSAGE]},"
                       f"{question[config.IMAGE]}\n")
    return None


def increment_question_view_number(question_id) -> None:
    questions = get_questions()
    with open(QUESTIONS_FILE_PATH, config.WRITE, encoding=config.UTF_8) as file:
        file.write(config.QUESTION_HEADER)
        for question in questions:
            if question[config.ID] == question_id:
                view_number = int(question[config.VIEW_NUMBER]) + 1
                question[config.VIEW_NUMBER] = view_number
            question[config.MESSAGE] = quote(question[config.MESSAGE])
            question[config.TITLE] = quote(question[config.TITLE])
            question[config.IMAGE] = quote(question[config.IMAGE])
            file.write(f"{question[config.ID]},"
                       f"{question[config.SUBMISSION_TIME]},"
                       f"{question[config.VIEW_NUMBER]},"
                       f"{question[config.VOTE_NUMBER]},"
                       f"{question[config.TITLE]},"
                       f"{question[config.MESSAGE]},"
                       f"{question[config.IMAGE]}\n")
    return None


def change_answer_vote(answer_id, direction) -> None:
    answers = get_answers()
    with open(ANSWERS_FILE_PATH, config.WRITE, encoding=config.UTF_8) as file:
        file.write(config.ANSWER_HEADER)
        for answer in answers:
            if answer[config.ID] == answer_id:
                vote_number = int(answer[config.VOTE_NUMBER])
                if direction == config.UP:
                    answer[config.VOTE_NUMBER] = vote_number + 1
                elif direction == config.DOWN:
                    answer[config.VOTE_NUMBER] = vote_number - 1
            answer[config.MESSAGE] = quote(answer[config.MESSAGE])
            answer[config.IMAGE] = quote(answer[config.IMAGE])
            file.write(f"{answer[config.ID]},"
                       f"{answer[config.SUBMISSION_TIME]},"
                       f"{answer[config.VOTE_NUMBER]},"
                       f"{answer[config.QUESTION_ID]},"
                       f"{answer[config.MESSAGE]},"
                       f"{answer[config.IMAGE]}\n")
    return None


def convert_line_brakes_to_br(text):
    return "\n".join(text.split("<br>"))
