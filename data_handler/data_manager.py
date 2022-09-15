from typing import List, Dict
import config
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

from data_handler import database_connection


@database_connection.connection_handler
def get_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_comments_for_question(cursor, question_id):
    query = """
        SELECT *
        FROM comment
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@database_connection.connection_handler
def get_comments_for_answers(cursor, answer_ids):
    answer_ids = tuple(answer_ids)
    query = """
        SELECT *
        FROM comment
        WHERE answer_id IN %(answer_ids)s""".format(answer_ids)
    cursor.execute(query, {"answer_ids": answer_ids})
    return cursor.fetchall()


@database_connection.connection_handler
def add_question(cursor, submission_time, title, message, image):
    query = """
        INSERT INTO question(submission_time, view_number, vote_number, title, message, image)
        VALUES (%(submission_time)s, 0, 0, %(title)s, %(message)s, %(image)s)
        """
    cursor.execute(query, {"submission_time": submission_time, "title": title, "message": message, "image": image})


@database_connection.connection_handler
def find_question(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id=%(question_id)s"""
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchone()


@database_connection.connection_handler
def find_answers_to_question(cursor, question_id):
    query = """
            SELECT * FROM answer
            WHERE question_id = %(question_id)s
            """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()



@database_connection.connection_handler
def add_answer(cursor, submission_time, question_id, message, image):
    query = """
        INSERT INTO answer(submission_time, vote_number, question_id, message, image)
        VALUES (%(submission_time)s, 0, %(question_id)s, %(message)s, %(image)s)
        """
    cursor.execute(query,
                   {"submission_time": submission_time, "question_id": question_id, "message": message, "image": image})


@database_connection.connection_handler
def add_comment_to_question(cursor, question_id, comment, submission_time):
    query = """
        INSERT INTO comment(question_id,answer_id, message, submission_time, edited_count)
        VALUES (%(question_id)s, NULL, %(comment)s, %(submission_time)s, 0)
        """
    cursor.execute(query,
                   {"question_id": question_id, "comment": comment, "submission_time": submission_time})


@database_connection.connection_handler
def add_comment_to_answer(cursor, answer_id, comment, submission_time):
    query = """
        INSERT INTO comment(answer_id, question_id, message, submission_time, edited_count)
        VALUES (%(answer_id)s, NULL, %(comment)s, %(submission_time)s, 0)
        """
    cursor.execute(query, {"answer_id": answer_id, "comment": comment, "submission_time": submission_time})


@database_connection.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE from answer
        WHERE question_id=%(question_id)s;
        
        DELETE from question
        WHERE id=%(question_id)s;"""
    cursor.execute(query, {"question_id": question_id})


@database_connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE from answer
        WHERE id=%(answer_id)s;
        
        DELETE from comment
        WHERE answer_id=%(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})


@database_connection.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE from comment
        WHERE id=%(comment_id)s"""
    cursor.execute(query, {"comment_id": comment_id})


@database_connection.connection_handler
def find_question_id_from_answer(cursor, answer_id):
    query = """
            SELECT question_id FROM answer
            WHERE id = %(answer_id)s
            """
    cursor.execute(query, {"answer_id": answer_id})
    return cursor.fetchone()


@database_connection.connection_handler
def find_question_id_from_comment(cursor, comment_id):
    query = """
            SELECT question_id FROM comment
            WHERE id = %(comment_id)s
            """
    cursor.execute(query, {"comment_id": comment_id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_question_image_name(cursor, question_id):
    query = """
            SELECT image FROM question
            WHERE id = %(question_id)s
            """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_answer_image_name(cursor, answer_id):
    query = """
            SELECT image FROM answer
            WHERE id = %(answer_id)s
            """
    cursor.execute(query, {"answer_id": answer_id})
    return cursor.fetchone()


@database_connection.connection_handler
def update_question(cursor, question_id, title, message, image):
    query = """
        UPDATE question
        SET title = %(title)s, message = %(message)s, image = %(image)s
        WHERE id=%(question_id)s"""
    cursor.execute(query, {"question_id": question_id, "title": title, "message": message, "image": image})


@database_connection.connection_handler
def update_question_vote(cursor, question_id, direction):
    if direction == config.UP:
        query = """
            UPDATE question
            SET vote_number = vote_number + 1
            WHERE id=%(question_id)s"""
        cursor.execute(query, {"question_id": question_id})
    elif direction == config.DOWN:
        query = """
            UPDATE question
            SET vote_number = vote_number - 1
            WHERE id=%(question_id)s"""
        cursor.execute(query, {"question_id": question_id})


@database_connection.connection_handler
def update_answer_vote(cursor, answer_id, direction):
    if direction == config.UP:
        query = """
            UPDATE answer
            SET vote_number = vote_number + 1
            WHERE id=%(answer_id)s"""
        cursor.execute(query, {"answer_id": answer_id})
    elif direction == config.DOWN:
        query = """
            UPDATE answer
            SET vote_number = vote_number - 1
            WHERE id=%(answer_id)s"""
        cursor.execute(query, {"answer_id": answer_id})


@database_connection.connection_handler
def increase_question_view_number(cursor, question_id):
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id=%(question_id)s"""
    cursor.execute(query, {"question_id": question_id})
