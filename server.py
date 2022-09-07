from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from werkzeug.utils import secure_filename
import os
import data_handler

UPLOAD_FOLDER = 'static'
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def list_questions():
    questions = data_handler.get_questions()
    return render_template('list.html', questions=questions)


@app.route("/question/<id>", methods=['GET', 'POST'])
def display_question(id):
    data_handler.higher_question_view_number(id)
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
        today = date.today()
        final_date = today.strftime("%d/%m/%Y")
        file = request.files['img']
        filename = save_file(file)
        data_handler.save_question({'id': index,
                                    'submission time': final_date,
                                    'view number': 0,
                                    'vote number': 0,
                                    'title': title,
                                    'message': question,
                                    'image': filename
                                    })
        return redirect(f'/question/{index}')
    return render_template('add_question.html')


def save_file(file):
    if 'img' in request.files and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = "no image"
    return filename


@app.route("/question/<id>/add-answer", methods=['GET', 'POST'])
def add_answer(id):
    if request.method == 'POST':
        answer = '"' + request.form['answer'] + '"'
        image = '"' + "None" + '"'
        index = len(data_handler.get_answers()) + 1
        today = date.today()
        final_date = today.strftime("%d/%m/%Y")
        data_handler.save_answer({'id': index,
                                  'submission time': final_date,
                                  'vote number': 0,
                                  'question id': id,
                                  'message': answer,
                                  'image': image,
                                  })
        return redirect(f'/question/{id}')
    return render_template('add_answer.html', question_id=id)


@app.route("/question/<id>/delete", methods=['GET', 'POST'])
def delete_question(id):
    all_questions = data_handler.get_questions()
    all_answers = data_handler.get_answers()
    for question in all_questions:
        if question['id'] == id:
            image = question['image']
            all_questions.remove(question)
            os.remove(f"static/{image}")
    index = 1
    for question in all_questions:
        question['id'] = str(index)
        index += 1
    for answer in all_answers:
        if answer['question id'] == id:
            all_answers.remove(answer)
    index = 1
    for answer in all_answers:
        answer['id'] = str(index)
        index += 1
    data_handler.update_answers(all_answers)
    data_handler.update_questions(all_questions)

    return redirect('/list')


@app.route("/answer/<answer_id>/delete", methods=['GET', 'POST'])
def delete_answer(answer_id):
    question_id = 0
    all_answers = data_handler.get_answers()
    for answer in all_answers:
        if answer['id'] == answer_id:
            all_answers.remove(answer)
            question_id = answer['question id']
    index = 1
    for answer in all_answers:
        answer['id'] = str(index)
        index += 1
    data_handler.update_answers(all_answers)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        today = date.today()
        final_date = today.strftime("%d/%m/%Y")
        file = request.files['img']
        filename = save_file(file)
        data_handler.edit_question({'id': question_id,
                                    'submission time': final_date,
                                    'view number': 0,
                                    'vote number': 0,
                                    'title': title,
                                    'message': question,
                                    'image': filename
                                    })
        return redirect(f'/question/{question_id}')
    all_questions = data_handler.get_questions()
    editable_question = {}
    for question in all_questions:
        if question['id'] == question_id:
            editable_question = question
    return render_template('edit_question.html', question=editable_question)


@app.route("/question/<question_id>/vote-up", methods=['GET', 'POST'])
def vote_question_up(question_id):
    data_handler.change_question_vote(question_id, "UP")
    return redirect("/list")


@app.route("/question/<question_id>/vote-down", methods=['GET', 'POST'])
def vote_question_down(question_id):
    data_handler.change_question_vote(question_id, "DOWN")
    return redirect("/list")


@app.route("/answer/<answer_id>/vote-up", methods=['GET', 'POST'])
def vote_answer_up(answer_id):
    all_answers = data_handler.get_answers()
    for answer in all_answers:
        if answer['id'] == answer_id:
            question_id = answer['question id']
    data_handler.change_answer_vote(answer_id, "UP")
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-down", methods=['GET', 'POST'])
def vote_answer_down(answer_id):
    all_answers = data_handler.get_answers()
    for answer in all_answers:
        if answer['id'] == answer_id:
            question_id = answer['question id']
    data_handler.change_answer_vote(answer_id, "DOWN")
    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run()
