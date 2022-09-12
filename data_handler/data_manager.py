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
def find_answer_to_question(cursor, question_id):
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
        WHERE id=%(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})


@database_connection.connection_handler
def find_question_id(cursor, answer_id):
    query = """
            SELECT question_id FROM answer
            WHERE id = %(answer_id)s
            """
    cursor.execute(query, {"answer_id": answer_id})
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

#
#
# @database_connection.connection_handler
# def get_applicants(cursor):
#     query = """
#         SELECT first_name, last_name, phone_number, application_code
#         FROM applicant
#         ORDER BY first_name"""
#     cursor.execute(query)
#     return cursor.fetchall()
#
#
# @database_connection.connection_handler
# def get_applicants_by_last_name(cursor, last_name):
#     query = """
#         SELECT first_name, last_name, phone_number
#         FROM applicant
#         WHERE last_name=%(surname)s
#         ORDER BY first_name"""
#     cursor.execute(query, {"surname": last_name})
#     return cursor.fetchall()
#
# @database_connection.connection_handler
# def get_applicants_by_code(cursor, code):
#     query = """
#         SELECT first_name, last_name, phone_number, email, application_code
#         FROM applicant
#         WHERE application_code=%(code)s
#         ORDER BY first_name"""
#     cursor.execute(query, {"code": code})
#     return cursor.fetchone()
#
# @database_connection.connection_handler
# def update_applicant_phone_number(cursor, code, new_number):
#     query = """
#         UPDATE applicant
#         SET phone_number = %(new_number)s
#         WHERE application_code=%(code)s"""
#     cursor.execute(query, {"code": code, "new_number": new_number})
#
# @database_connection.connection_handler
# def delete_applicant(cursor, code):
#     query = """
#         DELETE from applicant
#         WHERE application_code=%(code)s"""
#     cursor.execute(query, {"code": code})
#
#
#
# @database_connection.connection_handler
# def get_applicants_by_email(cursor, email):
#     query = """
#         SELECT first_name, last_name, phone_number
#         FROM applicant
#         WHERE email=%(email)s
#         ORDER BY first_name"""
#     cursor.execute(query, {"email": email})
#     return cursor.fetchall()
#
#
# @database_connection.connection_handler
# def get_mentors_by_last_name(cursor, last_name):
#     query = """
#         SELECT first_name, last_name, city
#         FROM mentor
#         WHERE last_name=%(surname)s
#         ORDER BY first_name"""
#     cursor.execute(query, {"surname": last_name})
#     return cursor.fetchall()
#
#
# @database_connection.connection_handler
# def get_mentors_by_city_name(cursor, name):
#     query = """
#         SELECT first_name, last_name, city
#         FROM mentor
#         WHERE city=%(city_name)s
#         ORDER BY first_name"""
#     cursor.execute(query, {"city_name": name})
#     return cursor.fetchall()
#
#
# @database_connection.connection_handler
# def get_cities(cursor):
#     query = """SELECT DISTINCT city FROM mentor"""
#     cursor.execute(query)
#     return cursor.fetchall()