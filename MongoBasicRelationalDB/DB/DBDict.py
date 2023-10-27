"""
This file manages all Reference/Normalization Mongo No SQL functions
Invoke this file to get customs JSONs or manage DB.py file to work.
"""

from . import DB
from datetime import datetime # TODO check date implementation

collection_names = ["Student", "Comment", "Article"]


# drop all database
def reset_setup():
    for collection in collection_names:
        DB.drop_collection(collection)
        DB.create_collection(collection)


# INSERT
#  Inserts a student into Student collection
def insert_student(name: str, s_name: str, user: str, password: str, no_approves=0, no_articles=0):
    return DB.insert_into_collection(collection_names[0],
                                     {"name": name, "s_name": s_name, "no_approves": no_approves, "no_articles": no_articles, "user": user,
                                      "password": password})


# insert multiple students in one single call to DB
def insert_students(students_dictionary: list[dict]):
    return insert_many_collection(collection_names[0], students_dictionary)


#  Inserts an article into Article collection
def insert_article(title: str, article: str, n_date: datetime, student_id: str, student_id_auth: str):
    return DB.insert_into_collection(collection_names[2], {"title": title, "article": article, "date":n_date, "student_id": student_id, "student_id_auth": student_id_auth})


# insert multiple articles in one single call to DB
def insert_articles(articles_dictionary: dict):
    return insert_many_collection(collection_names[2], articles_dictionary)


# insert a comment int Comment collection
def insert_comment(comment:str, date:datetime, student_id:str, article_id:str):
    return DB.insert_into_collection(collection_names[1], {"comment":comment, "date":date, "student_id":student_id,"article_id":article_id})


# insert multiple comments in one single call to DB
def insert_comments(comments_dictionary: dict):
    return insert_many_collection(collection_names[1], comments_dictionary)


def insert_many_collection(collection: str, data: list[dict]):
    return DB.insert_many_into_collection(collection, data)


# READ
# searches for all students, send a value into limit if u want to limit the query result
def find_students(query=None, args=None):
    return find_all_by_collection(collection_names[0], query, args)


# searches 1st student
def find_first_student():
    return find_one_by_collection(collection_names[0])


# search for all comments, send a value into limit if u want to limit the query result
def find_comments(query=None, args=None):
    return find_all_by_collection(collection_names[1], query, args)


def find_first_comment():
    return find_one_by_collection(collection_names[1])


# search for all comments, send a value into limit if u want to limit the query result
def find_articles(query=None, args=None):
    return find_all_by_collection(collection_names[2], query, args)


def find_first_article():
    return find_one_by_collection(collection_names[2])


# find rows into a collection for this project schema
def find_all_by_collection(collection: str, query=None, args=None):
    try:
        if query is None:
            return DB.find_all(collection)
        else:
            return DB.find_all(collection, True, query, args)
    except Exception as ex:
        raise Exception(f"Cannot get {collection} into DB\nError: {ex}")


def find_one_by_collection(collection: str):
    try:
        return DB.find_one(collection)
    except Exception as ex:
        raise Exception(f"Cannot get {collection} into DB\nError: {ex}")


# UPDATE
def update_student():
    return update_one_by_collection(collection_names[0])


def update_one_by_collection(collection: str, data):
    return



