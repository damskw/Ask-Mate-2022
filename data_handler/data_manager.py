from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_connection


# @database_connection.connection_handler
# def get_mentors(cursor):
#     query = """
#         SELECT first_name, last_name, city
#         FROM mentor
#         ORDER BY first_name"""
#     cursor.execute(query)
#     return cursor.fetchall()
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
