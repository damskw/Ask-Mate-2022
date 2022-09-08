from flask import Flask, render_template, request, redirect, url_for
from datetime import date
from werkzeug.utils import secure_filename
import config
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


@app.route("/question/<question_id>", methods=[config.GET, config.POST])
def display_question(question_id):
    data_handler.higher_question_view_number(question_id)
    question = data_handler.find_a_question(question_id)
    desired_answers = data_handler.find_answers(question_id)
    return render_template('display_question.html', question=question,
                           desired_answers=desired_answers)


@app.route("/add-question", methods=[config.GET, config.POST])
def add_question():
    if request.method == config.POST:
        title = config.QUOTATION_MARK + request.form[config.TITLE] + config.QUOTATION_MARK
        question = config.QUOTATION_MARK + request.form[config.QUESTION] + config.QUOTATION_MARK
        # question_id = len(data_handler.get_questions()) + 1
        question_ids = list(map(lambda question: question[config.ID], data_handler.get_questions()))
        print(question_ids)
        question_id = id_generator.generate_unique_id(question_ids, 3, 3, 3, 3)
        today = date.today()
        final_date = today.strftime("%d/%m/%Y")
        img_filename = save_image_file(request)
        data_handler.save_question({config.ID: question_id,
                                    config.SUBMISSION_TIME: final_date,
                                    config.VIEW_NUMBER: 0,
                                    config.VOTE_NUMBER: 0,
                                    config.TITLE: title,
                                    config.MESSAGE: question,
                                    config.IMAGE: img_filename
                                    })
        return redirect(f'/question/{question_id}')
    return render_template('add_question.html')


def save_image_file(request):
    img_filename = "no image"
    if config.IMG in request.files and request.files[config.IMG].filename != '':
        img_filename = secure_filename(request.files[config.IMG].filename)
        image = request.files[config.IMG]
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
    return img_filename


@app.route("/question/<question_id>/add-answer", methods=[config.GET, config.POST])
def add_answer(question_id):
    if request.method == config.POST:
        answer = config.QUOTATION_MARK + request.form[config.ANSWER] + config.QUOTATION_MARK
        image = config.QUOTATION_MARK + config.NONE + config.QUOTATION_MARK
        answer_ids = list(map(lambda question: question[config.ID], data_handler.get_questions()))
        answer_id = id_generator.generate_unique_id(answer_ids, 2, 2, 2, 2)
        # TODO: save in epoch
        today = date.today()
        final_date = today.strftime("%d/%m/%Y")
        data_handler.save_answer({config.ID: answer_id,
                                  config.SUBMISSION_TIME: final_date,
                                  config.VOTE_NUMBER: 0,
                                  config.QUESTION_ID: question_id,
                                  config.MESSAGE: answer,
                                  config.IMAGE: image,
                                  })
        return redirect(f'/question/{question_id}')
    return render_template('add_answer.html', question_id=question_id)


@app.route("/question/<question_id>/delete", methods=[config.GET, config.POST])
def delete_question(question_id):
    all_questions = data_handler.get_questions()
    all_answers = data_handler.get_answers()
    for question in all_questions:
        if question[config.ID] == question_id:
            image = question[config.IMAGE]
            if image != "" and os.path.exists(f"static/{image}"):
                os.remove(f"static/{image}")
            all_questions.remove(question)
    for answer in all_answers:
        if answer[config.QUESTION_ID] == question_id:
            all_answers.remove(answer)
    data_handler.update_answers(all_answers)
    data_handler.update_questions(all_questions)

    return redirect('/list')


@app.route("/answer/<answer_id>/delete", methods=[config.GET, config.POST])
def delete_answer(answer_id):
    question_id = None
    all_answers = data_handler.get_answers()
    for answer in all_answers:
        if answer[config.ID] == answer_id:
            question_id = answer[config.QUESTION_ID]
            all_answers.remove(answer)
    data_handler.update_answers(all_answers)
    if question_id is not None:
        return redirect(f'/question/{question_id}')
    else:
        return redirect('/')


@app.route("/question/<question_id>/edit", methods=[config.GET, config.POST])
def edit_question(question_id):
    if request.method == config.POST:
        title = request.form[config.TITLE]
        question = request.form[config.QUESTION]
        # do not change the submission date/time (I need to sort based on submission time),
        # we may create and use "last-modified" field instead for all the questions
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # today = date.today()
        # final_date = today.strftime("%d/%m/%Y")
        img_filename = save_image_file(request)
        data_handler.edit_question({config.ID: question_id,
                                    config.TITLE: title,
                                    config.MESSAGE: question,
                                    config.IMAGE: img_filename
                                    })
        return redirect(f'/question/{question_id}')
    all_questions = data_handler.get_questions()
    editable_question = {}
    for question in all_questions:
        if question[config.ID] == question_id:
            editable_question = question
    return render_template('edit_question.html', question=editable_question)


@app.route("/question/<question_id>/vote-up", methods=[config.GET, config.POST])
def vote_question_up(question_id):
    data_handler.change_question_vote(question_id, config.UP)
    return redirect("/list")


@app.route("/question/<question_id>/vote-down", methods=[config.GET, config.POST])
def vote_question_down(question_id):
    data_handler.change_question_vote(question_id, config.DOWN)
    return redirect("/list")


@app.route("/answer/<answer_id>/vote-up", methods=[config.GET, config.POST])
def vote_answer_up(answer_id):
    all_answers = data_handler.get_answers()
    for answer in all_answers:
        if answer[config.ID] == answer_id:
            question_id = answer[config.QUESTION_ID]
    data_handler.change_answer_vote(answer_id, config.UP)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-down", methods=[config.GET, config.POST])
def vote_answer_down(answer_id):
    all_answers = data_handler.get_answers()
    for answer in all_answers:
        if answer[config.ID] == answer_id:
            question_id = answer[config.QUESTION_ID]
    data_handler.change_answer_vote(answer_id, config.DOWN)
    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run()
