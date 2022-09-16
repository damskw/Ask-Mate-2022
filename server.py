from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import config
import os
from data_handler import data_handler, id_generator, data_manager
from utils import quote, convert_timestamp_to_utc

UPLOAD_FOLDER = 'static/images'
# app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# "{{url_for('static', filename='MD.png')}}"

@app.route("/list")
def list_questions():
    order_by = request.args.get("order_by", "submission_time")
    order_direction = request.args.get("order_direction", "desc")
    questions = data_manager.get_questions()
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == "desc"))
    return render_template('list.html', questions=questions)


@app.route("/")
def list_first_questions():
    order_by = request.args.get("order_by", "submission_time")
    order_direction = request.args.get("order_direction", "desc")
    questions = data_manager.get_questions()
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == "desc"))
    first_questions = questions[0:5]
    return render_template('list.html', questions=first_questions)


@app.route("/search")
def search_results():
    order_by = request.args.get("order_by", "submission_time")
    order_direction = request.args.get("order_direction", "desc")
    search_phrase = request.args.get("q", "None")
    questions = data_manager.find_results_by_search_phrase(search_phrase)
    questions.sort(key=lambda q: q[order_by], reverse=(order_direction == "desc"))
    if search_phrase == 'None':
        return render_template('search.html')
    return render_template('list.html', questions=questions, search_phrase=search_phrase)


@app.route("/question/<question_id>", methods=[config.GET, config.POST])
def display_question(question_id):
    question = data_manager.find_question(question_id)
    answers = data_manager.find_answers_to_question(question_id)
    answer_ids = []
    temp = [answer_ids.append(answer["id"]) for answer in answers]
    data_manager.increase_question_view_number(question_id)
    question_comments = data_manager.get_comments_for_question(question_id)
    print(answer_ids)
    if len(answer_ids) > 0:
        comments_for_answers = data_manager.get_comments_for_answers(answer_ids)
        return render_template('display_question.html', question=question, answers=answers,
                               question_comments=question_comments, comments_for_answers=comments_for_answers)
    if question:
        return render_template('display_question.html', question=question, answers=answers,
                               question_comments=question_comments)
    return render_template('404.html')


@app.route("/add-question", methods=[config.GET, config.POST])
def add_question():
    if request.method == config.POST:
        title = request.form[config.TITLE]
        question = request.form[config.QUESTION]
        now = datetime.now()
        timestamp = int(datetime.timestamp(now))
        img_filename = save_image_file(request, timestamp)
        data_manager.add_question(now, title, question, img_filename)
        return redirect('/')
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
    if request.method == config.GET:
        return render_template('add_answer.html', question_id=question_id)
    answer = request.form[config.ANSWER]
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    img_filename = save_image_file(request, timestamp)
    data_manager.add_answer(now, question_id, answer, img_filename)
    return redirect(f'/question/{question_id}')


@app.route("/comments/<comment_id>/delete", methods=[config.GET, config.POST])
def delete_comment(comment_id):
    question = data_manager.find_question_id_from_comment(comment_id)
    redirect_id = question[config.QUESTION_ID]
    if not isinstance(redirect_id, int):
        answer = data_manager.find_answer_id_from_comment(comment_id)
        answer_id = answer[config.ANSWER_ID]
        question = data_manager.find_question_id_from_answer(answer_id)
        redirect_id = question[config.QUESTION_ID]
    data_manager.delete_comment(comment_id)
    return redirect(f'/question/{redirect_id}')


@app.route("/question/<question_id>/new-comment", methods=[config.POST])
def add_comment_to_question(question_id):
    comment = request.form[config.QUESTION_COMMENT]
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    data_manager.add_comment_to_question(question_id, comment, now)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/new-comment", methods=[config.GET, config.POST])
def add_comment_to_answer(answer_id):
    if request.method == config.GET:
        return render_template('add_answer_comment.html', answer_id=answer_id)
    question = data_manager.find_question_id_from_answer(answer_id)
    question_id = question[config.QUESTION_ID]
    comment = request.form[config.QUESTION_COMMENT]
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    data_manager.add_comment_to_answer(answer_id, comment, now)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/delete", methods=[config.GET, config.POST])
def delete_question(question_id):
    question = data_manager.get_question_image_name(question_id)
    image_name = question[config.IMAGE]
    answers = data_manager.find_answers_to_question(question_id)
    answer_ids = []
    temp = [answer_ids.append(answer["id"]) for answer in answers]
    if len(answer_ids) > 0:
        data_manager.delete_all_answer_comments(answer_ids)
    data_manager.delete_question(question_id)
    if image_name != "" and os.path.exists(f"static/images/{image_name}"):
        os.remove(f"static/images/{image_name}")
    return redirect('/list')


@app.route("/answer/<answer_id>/delete", methods=[config.GET, config.POST])
def delete_answer(answer_id):
    question = data_manager.find_question_id_from_answer(answer_id)
    question_id = question[config.QUESTION_ID]
    question = data_manager.get_answer_image_name(answer_id)
    image_name = question[config.IMAGE]
    data_manager.delete_comment_from_answer(answer_id)
    data_manager.delete_answer(answer_id)
    if image_name != "" and os.path.exists(f"static/images/{image_name}"):
        os.remove(f"static/images/{image_name}")
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/edit", methods=[config.GET, config.POST])
def edit_question(question_id):
    if request.method == config.POST:
        title = request.form[config.TITLE]
        question = request.form[config.QUESTION]
        img_filename = save_image_file(request)
        data_manager.update_question(question_id, title, question, img_filename)
        return redirect(f'/question/{question_id}')
    question_to_be_edited = data_manager.find_question(question_id)
    return render_template('edit_question.html', question=question_to_be_edited)


@app.route("/answer/<answer_id>/edit", methods=[config.GET, config.POST])
def edit_answer(answer_id):
    if request.method == config.POST:
        question = data_manager.find_question_id_from_answer(answer_id)
        question_id = question[config.QUESTION_ID]
        answer = request.form[config.ANSWER]
        img_filename = save_image_file(request)
        data_manager.update_answer(answer_id, answer, img_filename)
        return redirect(f'/question/{question_id}')
    answer_to_be_edited = data_manager.find_answer(answer_id)
    return render_template('edit_answer.html', answer=answer_to_be_edited)


@app.route("/comment/<comment_id>/edit", methods=[config.GET, config.POST])
def edit_comment(comment_id):
    if request.method == config.POST:
        comment = request.form[config.COMMENT]
        data_manager.update_comment(comment_id, comment)
        data_manager.increase_comment_edit_number(comment_id)
        comment = data_manager.find_comment(comment_id)
        question_id = comment[config.QUESTION_ID]
        if not isinstance(question_id, int):
            answer_id = comment[config.ANSWER_ID]
            question = data_manager.find_question_id_from_answer(answer_id)
            question_id = question[config.QUESTION_ID]
        return redirect(f'/question/{question_id}')
    comment_to_be_edited = data_manager.find_comment(comment_id)
    return render_template('edit_comment.html', comment=comment_to_be_edited)



@app.route("/question/<question_id>/vote-up", methods=[config.GET, config.POST])
def vote_question_up(question_id):
    data_manager.update_question_vote(question_id, config.UP)
    # TODO (in the farther futures): do not redirect, only send a request with JS and update value of DOM based on
    #  response
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/vote-down", methods=[config.GET, config.POST])
def vote_question_down(question_id):
    data_manager.update_question_vote(question_id, config.DOWN)
    # TODO (in the farther futures): do not redirect, only send a request with JS and update value of DOM based on
    #  response
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-up", methods=[config.GET, config.POST])
def vote_answer_up(answer_id):
    data_manager.update_answer_vote(answer_id, config.UP)
    question = data_manager.find_question_id_from_answer(answer_id)
    question_id = question[config.QUESTION_ID]
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/vote-down", methods=[config.GET, config.POST])
def vote_answer_down(answer_id):
    data_manager.update_answer_vote(answer_id, config.DOWN)
    question = data_manager.find_question_id_from_answer(answer_id)
    question_id = question[config.QUESTION_ID]
    return redirect(f'/question/{question_id}')


@app.route("/404")
def display_404():
    return render_template("404.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
