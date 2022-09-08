from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from werkzeug.utils import secure_filename
import os
from data_handler import data_handler, id_generator

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
    question = data_handler.find_a_question(id)
    desired_answers = data_handler.find_answers(id)  # id is question's id
    return render_template('display_question.html', question=question,
                           desired_answers=desired_answers)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        title = '"' + request.form['title'] + '"'
        question = '"' + request.form['question'] + '"'
        # question_id = len(data_handler.get_questions()) + 1
        question_ids = list(map(lambda question: question["id"], data_handler.get_questions()))
        print(question_ids)
        question_id = id_generator.generate_unique_id(question_ids, 3, 3, 3, 3)
        today = date.today()
        final_date = today.strftime("%d/%m/%Y")
        img_filename = save_image_file(request)
        data_handler.save_question({'id': question_id,
                                    'submission time': final_date,
                                    'view number': 0,
                                    'vote number': 0,
                                    'title': title,
                                    'message': question,
                                    'image': img_filename
                                    })
        return redirect(f'/question/{question_id}')
    return render_template('add_question.html')


def save_image_file(request):
    img_filename = "no image"
    if 'img' in request.files and request.files['img'].filename != '':
        img_filename = secure_filename(request.files['img'].filename)
        image = request.files['img']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
    return img_filename


@app.route("/question/<id>/add-answer", methods=['GET', 'POST'])
def add_answer(id):  # id is question id
    if request.method == 'POST':
        answer = '"' + request.form['answer'] + '"'
        image = '"' + "None" + '"'
        answer_ids = list(map(lambda question: question["id"], data_handler.get_questions()))
        answer_id = id_generator.generate_unique_id(answer_ids, 2, 2, 2, 2)
        # TODO: save in epoch
        today = date.today()
        final_date = today.strftime("%d/%m/%Y")
        data_handler.save_answer({'id': answer_id,
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
            try:
                if image != "":
                    os.remove(f"static/{image}")
            except FileNotFoundError as err:
                print(err)
            all_questions.remove(question)
    for answer in all_answers:
        if answer['question id'] == id:
            all_answers.remove(answer)
    data_handler.update_answers(all_answers)
    data_handler.update_questions(all_questions)

    return redirect('/list')


@app.route("/answer/<answer_id>/delete", methods=['GET', 'POST'])
def delete_answer(answer_id):
    question_id = None
    all_answers = data_handler.get_answers()
    for answer in all_answers:
        if answer['id'] == answer_id:
            question_id = answer['question id']
            all_answers.remove(answer)
    data_handler.update_answers(all_answers)
    if question_id is not None:
        return redirect(f'/question/{question_id}')
    else:
        return redirect('/')

@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        # do not change the submission date/time (I need to sort based on submission time),
        # we may create and use "last-modified" field instead for all the questions
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # today = date.today()
        # final_date = today.strftime("%d/%m/%Y")
        img_filename = save_image_file(request)
        data_handler.edit_question({'id': question_id,
                                    'title': title,
                                    'message': question,
                                    'image': img_filename
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
