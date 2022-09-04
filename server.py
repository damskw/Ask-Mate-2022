from flask import Flask, render_template

import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    questions = data_handler.get_questions()
    return render_template('list.html', questions=questions)


@app.route("/question/<id>", methods=['GET', 'POST'])
def display_question(id):
    all_questions = data_handler.get_questions()
    question = data_handler.find_a_question(id)
    all_answers = data_handler.get_answers()
    desired_answers = data_handler.find_an_answer(id)
    return render_template('display_question.html', question=question,
                           questions=all_questions, answers=all_answers,
                           desired_answers=desired_answers)


if __name__ == "__main__":
    app.run()
