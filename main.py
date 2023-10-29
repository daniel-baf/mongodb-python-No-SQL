# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from DB import DBDict
import datetime


def print_data():
    # find on DB
    print("########## DATA ##########")
    print("---- STUDENTS ----")
    # all students
    list(map(lambda _doc: print(_doc), DBDict.find_students()))
    print("---- COMMENTS ----")
    # all comments
    list(map(lambda _doc: print(_doc), DBDict.find_comments()))
    print("---- ARTICLES ----")
    # all articles
    list(map(lambda _doc: print(_doc), DBDict.find_articles()))
    print("")


def insert_examples():
    print("---- INSERT EXAMPLES ----")
    # insert
    DBDict.insert_student("Atol", "De elote", "atde", "abc123", 0, 0)  # return the inserted id
    data = [
        {"name": "Daniel", "s_name": "Bautista", "no_approves": 1, "no_articles": 0, "user": "daba",
         "password": "123abc"},
        {"name": "Pablo", "s_name": "Coti", "no_approves": 0, "no_articles": 1, "user": "paco", "password": "abc123"}]
    ids_usr = DBDict.insert_students(data)
    # note: use this to get 1 element, so we reuse code DBDict.find_students({"_id":id})[0]
    article_id = DBDict.insert_article("Pistachos", "Lorem ipsum dolor sit amet . Ametecessitatibus repellendus.",
                                       datetime.datetime.now(), ids_usr[1], ids_usr[0])
    DBDict.insert_comment("Quidem, voluptas laudantium. Molestiae.", datetime.datetime.now(), ids_usr[0], article_id)


def search_examples():
    print("---- READ EXAMPLES ----")
    print("Get first")
    print(DBDict.find_first_student())  # find_first_comment && find_first_article exists

    print("FILTER RESULTS")
    list(map(lambda _doc: print(_doc), DBDict.find_students(
        {"_id": 0, "name": 1})))  # search and return only "name", _id is always returned, add 0 to hide

    print("FILTERS + ARGUMENTS")  # send None instead of dict if no filter required + arguments
    # search and return only "name", _id is always returned, add 0 to hide
    list(map(lambda _doc: print(_doc), DBDict.find_students({"_id": 0, "name": 1, "s_name": 1}, {"name": "Pablo"})))


def update_examples():
    print("---- INSERT EXAMPLES ----")
    print("update single")  # also, exists function update_article, update_comment... send True
    # 3rd parameter to update multiple matches
    DBDict.update_student({"name": "Daniel"}, {"s_name": "Chorizo"})


def delete_examples():
    print("---- DELETE EXAMPLES ----")
    DBDict.delete_student({"name": "Atol"})  # also exist delete_article... send 2nd param true if delete multiple lines


def run():
    # Use a breakpoint in the code line below to debug your script.
    # reset DB for testing
    DBDict.reset_setup()
    print_data()
    insert_examples()
    print_data()
    search_examples()
    update_examples()
    print_data()
    delete_examples()
    print_data()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        run()
    except Exception as ex:
        print(f"Unable to run app, error: {ex}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
