from flask import Flask, render_template

import data_handler

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_questions():
    questions = data_handler.get_questions()
    # for question in questions:
    #     question["message"] = data_handler.convert_line_brakes_to_br(question["message"])
    return render_template('list.html', questions=questions)


if __name__ == "__main__":
    app.run()
