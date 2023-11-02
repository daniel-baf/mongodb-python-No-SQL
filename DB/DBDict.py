"""
This file manages all Reference/Normalization Mongo No SQL functions
Invoke this file to get customs JSONs or manage DB.py file to work.
"""

from . import DB
from datetime import datetime  # TODO check date implementation

collection_names = ["Student", "Comment", "Article"]


# drop all database
def reset_setup():
    for collection in collection_names:
        DB.drop_collection(collection)
        DB.create_collection(collection)


# INSERT
#  Inserts a student into Student collection
def insert_student(name: str, last_name: str, user: str, password: str, no_approves=0, no_articles=0, no_comments=0):
    return DB.insert_into_collection(collection_names[0],
                                     {"name": name, "last_name": last_name, "no_approves": no_approves,
                                      "no_articles": no_articles, "no_comments": no_comments, "user": user,
                                      "password": password})


# insert multiple students in one single call to DB
def insert_students(students_dictionary: list[dict]):
    return insert_many_collection(collection_names[0], students_dictionary)


#  Inserts an article into Article collection
def insert_article(title: str, article: str, n_date: datetime, student_id: str, student_id_auth: str):
    return DB.insert_into_collection(collection_names[2],
                                     {"title": title, "article": article, "date": n_date, "student_id": student_id,
                                      "student_id_auth": student_id_auth})


# insert multiple articles in one single call to DB
def insert_articles(articles_dictionary: list[dict]):
    return insert_many_collection(collection_names[2], articles_dictionary)


# insert a comment int Comment collection
def insert_comment(comment: str, date: datetime, student_id: str, article_id: str):
    return DB.insert_into_collection(collection_names[1], {"comment": comment, "date": date, "student_id": student_id,
                                                           "article_id": article_id})


# insert multiple comments in one single call to DB
def insert_comments(comments_dictionary: list[dict]):
    return insert_many_collection(collection_names[1], comments_dictionary)


# generic function to call DB file, insert many rows on a single DB call
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
# query = the data u want each row to return, None = all cells
# args = filter search, usually send id, but can send any element
def find_comments(query=None, args=None):
    return find_all_by_collection(collection_names[1], query, args)


# return 1st comment on Comment collection
def find_first_comment():
    return find_one_by_collection(collection_names[1])


# search for all comments, send a value into limit if u want to limit the query result
def find_articles(query=None, args=None):
    return find_all_by_collection(collection_names[2], query, args)


# return 1st article in Article collection
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
# updates student collection, search_query = the find parameters, updated_data = new data attrs to update
# update_many, send true if update all searched items on collection, otherwise, updates only first match if exists
def update_student(search_query: dict, updated_data: dict, update_many=False):
    return update_document(collection_names[0], search_query, updated_data, update_many)


# update comment collection, search_query = the find parameters, updated_data = new data attrs to update
# update_many, send true if update all searched items on collection, otherwise, updates only first match if exists
def update_comment(search_query: dict, updated_data: dict, update_many=False):  # TODO do update
    return update_document(collection_names[1], search_query, updated_data, update_many)


# update article collection, search_query = the find parameters, updated_data = new data attrs to update
# update_many, send true if update all searched items on collection, otherwise, updates only first match if exists
def update_article(search_query: dict, updated_data: dict, update_many=False):  # TODO do update
    return update_document(collection_names[2], search_query, updated_data, update_many)


# generic function, this function calls the DB file and run file, search_query = the find parameters, updated_data =
# new data attrs to update update_many, send true if update all searched items on collection, otherwise, updates only
# first match if exists
def update_document(collection: str, query: dict, data: dict, use_many=False):
    return DB.update(collection, query, data, use_many)


# DELETE
# delete a student document, delete any row that matches with filters
def delete_student(filter_document: dict, delete_many=False):
    return delete_document(collection_names[0], filter_document, delete_many)


# delete a comment document, delete any row that matches with filters
def delete_comment(filter_document: dict, delete_many=False):
    return delete_document(collection_names[1], filter_document, delete_many)


# delete an article document, delete any row that matches with filters
def delete_article(filter_document: dict, delete_many=False):
    return delete_document(collection_names[2], filter_document, delete_many)


# generic function to delete a collection, delete all matches with filter dict, and return no. rows afected
def delete_document(collection: str, filter_document: dict, delete_many=False):
    return DB.delete(collection, filter_document, delete_many)
