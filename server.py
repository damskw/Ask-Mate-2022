import random

from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from werkzeug.utils import secure_filename
import config
import os
from data_handler import data_manager
import bcrypt as bcrypt

UPLOAD_FOLDER = 'static/images'
# app = Flask(__name__, static_url_path='/static')
app = Flask(__name__)
app.secret_key = "tabaluga"
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
    tag_ids_raw = data_manager.get_question_tag_ids(question_id)
    tag_ids = []
    [tag_ids.append(tag[config.TAG_ID]) for tag in tag_ids_raw]
    tags_for_question = data_manager.get_tags_from_tag_ids(tag_ids)
    question = data_manager.find_question(question_id)
    answers = data_manager.find_answers_to_question(question_id)
    answer_ids = []
    [answer_ids.append(answer[config.ID]) for answer in answers]
    question_comments = data_manager.get_comments_for_question(question_id)
    comments_for_answers = data_manager.get_comments_for_answers(answer_ids)
    if request.method == config.POST:
        data_manager.increase_question_view_number(question_id)
    if question:
        return render_template('display_question.html', question=question, answers=answers,
                               question_comments=question_comments, tags_for_question=tags_for_question,
                               comments_for_answers=comments_for_answers)
    return render_template('404.html')


@app.route("/add-question", methods=[config.GET, config.POST])
def add_question():
    if request.method == config.GET:
        return render_template('add_question.html')

    title = request.form[config.TITLE]
    question = request.form[config.QUESTION]
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    img_filename = save_image_file(request, timestamp)
    data_manager.add_question(now, title, question, img_filename)
    return redirect('/')


@app.route("/question/<question_id>/new-tag", methods=[config.GET, config.POST])
def new_question_tag(question_id):
    if request.method == config.GET:
        all_tags = data_manager.get_all_tags()
        return render_template('new_tag.html', tags=all_tags, question_id=question_id)

    tag = request.form[config.QUESTION_TAG]
    if tag == "":
        return redirect(f'/question/{question_id}')
    full_tag = data_manager.find_tag_by_name(tag)
    if full_tag is None:
        data_manager.create_new_tag(tag)
        full_tag = data_manager.find_tag_by_name(tag)
    tag_id = full_tag[config.ID]
    exist = data_manager.check_if_tag_id_already_in_question(question_id, tag_id)
    print(exist)
    if len(exist) == 0:
        data_manager.add_tag_to_a_question(question_id, tag_id)
    return redirect(f'/question/{question_id}')


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
    # timestamp = int(datetime.timestamp(now))
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
    # timestamp = int(datetime.timestamp(now))
    data_manager.add_comment_to_answer(answer_id, comment, now)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/delete", methods=[config.GET, config.POST])
def delete_question(question_id):
    question = data_manager.get_question_image_name(question_id)
    image_name = question[config.IMAGE]
    answers = data_manager.find_answers_to_question(question_id)
    answer_ids = []
    [answer_ids.append(answer[config.ID]) for answer in answers]
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


@app.route("/question/<question_id>/tag/<tag_id>/delete", methods=[config.GET, config.POST])
def delete_tag_from_question(question_id, tag_id):
    data_manager.remove_tag_from_question(question_id, tag_id)
    return redirect(f'/question/{question_id}')


@app.route("/question/<question_id>/edit", methods=[config.GET, config.POST])
def edit_question(question_id):
    if request.method == config.GET:
        question_to_be_edited = data_manager.find_question(question_id)
        return render_template('edit_question.html', question=question_to_be_edited)

    title = request.form[config.TITLE]
    question = request.form[config.QUESTION]
    img_filename = save_image_file(request)
    data_manager.update_question(question_id, title, question, img_filename)
    return redirect(f'/question/{question_id}')


@app.route("/answer/<answer_id>/edit", methods=[config.GET, config.POST])
def edit_answer(answer_id):
    if request.method == config.GET:
        answer_to_be_edited = data_manager.find_answer(answer_id)
        return render_template('edit_answer.html', answer=answer_to_be_edited)

    question = data_manager.find_question_id_from_answer(answer_id)
    question_id = question[config.QUESTION_ID]
    answer = request.form[config.ANSWER]
    img_filename = save_image_file(request)
    data_manager.update_answer(answer_id, answer, img_filename)
    return redirect(f'/question/{question_id}')


@app.route("/comment/<comment_id>/edit", methods=[config.GET, config.POST])
def edit_comment(comment_id):
    if request.method == config.GET:
        comment_to_be_edited = data_manager.find_comment(comment_id)
        return render_template('edit_comment.html', comment=comment_to_be_edited)

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


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def is_loggedin():
    return 'user_email' in session


def create_random_user_id():
    id = random.randint(1, 1000000000)
    return id


@app.route("/register", methods=[config.GET, config.POST])
def register():
    if session:
        return redirect('/')
    if request.method == config.GET:
        return render_template('register.html')
    email = request.form.get('email')
    password = request.form.get('password')
    repeated_password = request.form.get('repeat-password')
    now = datetime.now()
    user_id = create_random_user_id()
    name = "User" + str(user_id)
    check_email = data_manager.check_if_user_email_in_database(email)
    if check_email is not None:
        return render_template('register.html', message="This e-mail is already registered")
    if password != repeated_password:
        return render_template('register.html', message="Please check your password")
    data_manager.register_user(email, hash_password(password), now, name)
    return redirect('/')


@app.route("/login", methods=[config.GET, config.POST])
def login():
    if session:
        return redirect('/')
    if request.method == config.GET:
        return render_template('login.html')
    email = request.form.get('email')
    user = data_manager.login(email)
    if not user:
        return render_template('register.html', message="Unknown e-mail, please register.")
    password = request.form.get('password')
    if verify_password(password, user["password"]):
        session["user_email"] = email
        return redirect('/')
    return render_template('login.html', message='Wrong password!')


@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect('/')


@app.route("/404")
def display_404():
    return render_template("404.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
