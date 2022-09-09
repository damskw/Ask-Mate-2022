from flask import Flask, render_template, request, redirect
from datetime import datetime
from werkzeug.utils import secure_filename
import config
import os
from data_handler import data_handler, id_generator
from utils import quote, convert_timestamp_to_utc

UPLOAD_FOLDER = 'static'
app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def list_questions():
    order_by = request.args.get("order_by", "title")
    order_direction = request.args.get("order_direction", "desc")
    questions = data_handler.get_questions()
    for question in questions:
        try:
            question[config.SUBMISSION_TIME] = convert_timestamp_to_utc(question.get(config.SUBMISSION_TIME))
        except ValueError:
            question[config.SUBMISSION_TIME] = ""
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == "desc"))
    return render_template('list.html', questions=questions)


@app.route("/question/<question_id>", methods=[config.GET, config.POST])
def display_question(question_id):
    data_handler.increment_question_view_number(question_id)
    question = data_handler.get_question(question_id)
    try:
        question[config.SUBMISSION_TIME] = convert_timestamp_to_utc(question.get(config.SUBMISSION_TIME))
    except ValueError:
        question[config.SUBMISSION_TIME] = ""
    desired_answers = data_handler.get_answers_to_question(question_id)
    if desired_answers is not None:
        for answer in desired_answers:
            try:
                answer[config.SUBMISSION_TIME] = convert_timestamp_to_utc(answer.get(config.SUBMISSION_TIME))
            except ValueError:
                answer[config.SUBMISSION_TIME] = ""
    return render_template('display_question.html', question=question,
                           desired_answers=desired_answers)


@app.route("/add-question", methods=[config.GET, config.POST])
def add_question():
    if request.method == config.POST:
        title = quote(request.form[config.TITLE])
        question = quote(request.form[config.QUESTION])
        question_ids = list(map(lambda question: question[config.ID], data_handler.get_questions()))
        question_id = id_generator.generate_unique_id(question_ids, 3, 3, 3, 3)
        now = datetime.now()
        timestamp = int(datetime.timestamp(now))
        img_filename = save_image_file(request, timestamp)
        data_handler.save_question({config.ID: question_id,
                                    config.SUBMISSION_TIME: timestamp,
                                    config.VIEW_NUMBER: 0,
                                    config.VOTE_NUMBER: 0,
                                    config.TITLE: title,
                                    config.MESSAGE: question,
                                    config.IMAGE: img_filename
                                    })
        return redirect(f'/question/{question_id}')
    return render_template('add_question.html')


def save_image_file(request, timestamp: int = None) -> str:
    img_filename = ""
    if config.IMG in request.files and request.files[config.IMG].filename != '':
        print("Detected img in the request.")
        if timestamp is None:
            now = datetime.now()
            timestamp = int(datetime.timestamp(now))
        img_filename = str(timestamp) + secure_filename(request.files[config.IMG].filename)
        image = request.files[config.IMG]
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
    return img_filename


@app.route("/question/<question_id>/add-answer", methods=[config.GET, config.POST])
def add_answer(question_id):
    if request.method == config.POST:
        answer = quote(request.form[config.ANSWER])
        answer_ids = list(map(lambda question: question[config.ID], data_handler.get_questions()))
        answer_id = id_generator.generate_unique_id(answer_ids, 2, 2, 2, 2)
        now = datetime.now()
        timestamp = int(datetime.timestamp(now))
        img_filename = save_image_file(request, timestamp)
        data_handler.save_answer({config.ID: answer_id,
                                  config.SUBMISSION_TIME: timestamp,
                                  config.VOTE_NUMBER: 0,
                                  config.QUESTION_ID: question_id,
                                  config.MESSAGE: answer,
                                  config.IMAGE: img_filename,
                                  })
        return redirect(f'/question/{question_id}')
    return render_template('add_answer.html', question_id=question_id)


@app.route("/question/<question_id>/delete", methods=[config.GET, config.POST])
def delete_question(question_id):
    all_questions = data_handler.get_questions()
    try:
        question_to_delete = next(filter(lambda question: question[config.ID] == question_id, all_questions))
    except StopIteration:
        return redirect('/404')
    image_name = question_to_delete[config.IMAGE]
    if image_name != "" and os.path.exists(f"static/{image_name}"):
        os.remove(f"static/{image_name}")
    all_questions.remove(question_to_delete)
    all_answers = data_handler.get_answers()
    answers_to_this_question = data_handler.get_answers_to_question(question_id)
    for answer in answers_to_this_question:
        all_answers.remove(answer)
    data_handler.update_answers(all_answers)
    data_handler.update_questions(all_questions)

    return redirect('/list')


@app.route("/answer/<answer_id>/delete", methods=[config.GET, config.POST])
def delete_answer(answer_id):
    all_answers = data_handler.get_answers()
    try:
        answer = next(filter(lambda answer: answer[config.ID] == answer_id, all_answers))
    except StopIteration:
        return redirect("/404")
    image_name = answer[config.IMAGE]
    if image_name != "" and os.path.exists(f"static/{image_name}"):
        os.remove(f"static/{image_name}")
    question_id = answer[config.QUESTION_ID]
    question = data_handler.get_question(question_id)
    all_answers.remove(answer)
    data_handler.update_answers(all_answers)
    if question is not None:
        return redirect(f'/question/{question_id}')
    else:
        return redirect('/')


@app.route("/question/<question_id>/edit", methods=[config.GET, config.POST])
def edit_question(question_id):
    if request.method == config.POST:
        title = request.form[config.TITLE]
        question = request.form[config.QUESTION]
        img_filename = save_image_file(request)
        data_handler.edit_question({config.ID: question_id,
                                    config.TITLE: title,
                                    config.MESSAGE: question,
                                    config.IMAGE: img_filename
                                    })
        return redirect(f'/question/{question_id}')
    question_to_be_edited = data_handler.get_question(question_id)
    return render_template('edit_question.html', question=question_to_be_edited)


@app.route("/question/<question_id>/vote-up", methods=[config.GET, config.POST])
def vote_question_up(question_id):
    data_handler.change_question_vote(question_id, config.UP)
    # TODO (in the farther futures): do not redirect, only send a request with JS and update value of DOM based on
    #  response
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/vote-down", methods=[config.GET, config.POST])
def vote_question_down(question_id):
    data_handler.change_question_vote(question_id, config.DOWN)
    # TODO (in the farther futures): do not redirect, only send a request with JS and update value of DOM based on
    #  response
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-up", methods=[config.GET, config.POST])
def vote_answer_up(answer_id):
    answer = data_handler.get_answer(answer_id)
    question_id = answer[config.QUESTION_ID]
    data_handler.change_answer_vote(answer_id, config.UP)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-down", methods=[config.GET, config.POST])
def vote_answer_down(answer_id):
    answer = data_handler.get_answer(answer_id)
    question_id = answer[config.QUESTION_ID]
    data_handler.change_answer_vote(answer_id, config.DOWN)
    return redirect(f'/question/{question_id}')


@app.route("/404")
def display_404():
    return render_template("404.html")


if __name__ == "__main__":
    app.run()
