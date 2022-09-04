from flask import Flask, render_template, request, redirect

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


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        title = '"' + request.form['title'] + '"'
        question = '"' + request.form['question'] + '"'
        index = len(data_handler.get_questions()) + 1
        data_handler.save_question({'id': index,
                                    'submission time': 0,
                                    'view number': 0,
                                    'vote number': 0,
                                    'title': title,
                                    'message': question,
                                    'image': 'None'
                                    })
        return redirect(f'/question/{index}')
    return render_template('add_question.html')


if __name__ == "__main__":
    app.run()
