from typing import List, Dict
import config
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

from data_handler import database_connection


@database_connection.connection_handler
def get_data(cursor, table_name, order_by = None):
    variables = {}
    query = f"SELECT * FROM {table_name}"

    if order_by: 
        query += " ORDER BY %(order_by)s"
        variables['order_by'] = order_by
    
    cursor.execute(query, variables)
    return cursor.fetchall()

# get question: get_data('question')
# get all tags: get_data('tag', 'id')

@database_connection.connection_handler
def get_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY id"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_tags(cursor):
    query = """
        SELECT *
        FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_tag_ids(cursor, question_id):
    query = """
        SELECT *
        FROM question_tag
        WHERE question_id = %(question_id)s"""
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@database_connection.connection_handler
def add_tag_to_a_question(cursor, question_id, tag_id):
    query = """
        INSERT INTO question_tag(question_id, tag_id)
        VALUES (%(question_id)s, %(tag_id)s)
        """
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


@database_connection.connection_handler
def create_new_tag(cursor, tag):
    query = """
        INSERT INTO tag(name)
        VALUES (%(tag)s)
        """
    cursor.execute(query, {"tag": tag})


@database_connection.connection_handler
def find_tag_by_name(cursor, tag):
    query = """
        SELECT *
        FROM tag
        WHERE name=%(tag)s
        """
    cursor.execute(query, {"tag": tag})
    return cursor.fetchone()


@database_connection.connection_handler
def find_results_by_search_phrase(cursor, phrase):
    phrase = '%' + phrase.lower() + '%'
    query = """
            SELECT * 
            FROM question
            WHERE LOWER(title) LIKE %(phrase)s OR LOWER(message) LIKE %(phrase)s
            """
    cursor.execute(query, {"phrase": phrase})
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
    query = "SELECT * FROM comment"

    if len(answer_ids) > 1:
        answer_ids = tuple(answer_ids)
        query += " WHERE answer_id IN %(answer_ids)s"
    elif len(answer_ids) == 1:
        answer_ids = answer_ids[0]
        query += " WHERE answer_id=%(answer_ids)s"
    else:
        return []
    cursor.execute(query, {"answer_ids": answer_ids})
    return cursor.fetchall()


@database_connection.connection_handler
def check_if_tag_id_already_in_question(cursor, question_id, tag_id):
    query = """
        SELECT *
        FROM question_tag
        WHERE tag_id=%(tag_id)s AND question_id=%(question_id)s"""
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})
    return cursor.fetchall()


@database_connection.connection_handler
def get_tags_from_tag_ids(cursor, tag_ids):
    if len(tag_ids) > 1:
        tag_ids = tuple(tag_ids)
        query = """
            SELECT *
            FROM tag
            WHERE id IN %(tag_ids)s"""
    elif len(tag_ids) == 1:
        tag_ids = tag_ids[0]
        query = """
            SELECT *
            FROM tag
            WHERE id=%(tag_ids)s"""
    else:
        return []
    cursor.execute(query, {"tag_ids": tag_ids})
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
def find_answer(cursor, answer_id):
    query = """
        SELECT *
        FROM answer
        WHERE id=%(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})
    return cursor.fetchone()


@database_connection.connection_handler
def find_comment(cursor, comment_id):
    query = """
        SELECT *
        FROM comment
        WHERE id=%(comment_id)s"""
    cursor.execute(query, {"comment_id": comment_id})
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
        DELETE from question_tag
        WHERE question_id=%(question_id)s;
    
        DELETE from comment
        WHERE question_id=%(question_id)s;
    
        DELETE from answer
        WHERE question_id=%(question_id)s;
        
        DELETE from question
        WHERE id=%(question_id)s;"""
    cursor.execute(query, {"question_id": question_id})


@database_connection.connection_handler
def delete_all_answer_comments(cursor, answer_ids):
    if len(answer_ids) > 1:
        answer_ids = tuple(answer_ids)
        query = """
            DELETE from comment
            WHERE answer_id IN %(answer_ids)s;"""
    elif len(answer_ids) == 1:
        answer_ids = answer_ids[0]
        query = """
            DELETE from comment
            WHERE answer_id=%(answer_ids)s;"""
    else:
        return
    cursor.execute(query, {"answer_ids": answer_ids})


@database_connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE from answer
        WHERE id=%(answer_id)s;
        
        DELETE from comment
        WHERE answer_id=%(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})


@database_connection.connection_handler
def remove_tag_from_question(cursor, question_id, tag_id):
    query = """
        DELETE from question_tag
        WHERE question_id=%(question_id)s AND tag_id=%(tag_id)s;"""
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


@database_connection.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE from comment
        WHERE id=%(comment_id)s"""
    cursor.execute(query, {"comment_id": comment_id})


@database_connection.connection_handler
def delete_comment_from_answer(cursor, answer_id):
    query = """
        DELETE from comment
        WHERE answer_id=%(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id})


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
def find_answer_id_from_comment(cursor, comment_id):
    query = """
            SELECT answer_id FROM comment
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
def update_answer(cursor, answer_id, message, image):
    query = """
        UPDATE answer
        SET message = %(message)s, image = %(image)s
        WHERE id=%(answer_id)s"""
    cursor.execute(query, {"answer_id": answer_id, "message": message, "image": image})


@database_connection.connection_handler
def update_comment(cursor, comment_id, message):
    query = """
        UPDATE comment
        SET message = %(message)s
        WHERE id=%(comment_id)s"""
    cursor.execute(query, {"comment_id": comment_id, "message": message})


@database_connection.connection_handler
def update_question_vote(cursor, question_id, direction):
    vote  = 1 if direction == config.UP else -1
    query = """
        UPDATE question
        SET vote_number = vote_number + %(vote)s
        WHERE id=%(question_id)s"""
    cursor.execute(query, {"question_id": question_id, "vote": vote})


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


@database_connection.connection_handler
def increase_comment_edit_number(cursor, comment_id):
    query = """
        UPDATE comment
        SET edited_count = edited_count + 1
        WHERE id=%(comment_id)s"""
    cursor.execute(query, {"comment_id": comment_id})


@database_connection.connection_handler
def check_if_user_email_in_database(cursor, email):
    query = """
        SELECT email
        FROM public."user"
        WHERE email=%(email)s"""
    cursor.execute(query, {"email": email})
    return cursor.fetchone()


@database_connection.connection_handler
def register_user(cursor, email, hashed_password, creation_date, name):
    query = """
    INSERT INTO public.user(email, password, name, role, member_since, avatar, last_log_in, location, about_me, reputation)
    VALUES (%(email)s, %(hashed_password)s, %(name)s, 'user', %(creation_date)s, null, %(creation_date)s, null, null, 0)"""
    cursor.execute(query, {'email': email, 'hashed_password': hashed_password, 'creation_date': creation_date, 'name': name})
