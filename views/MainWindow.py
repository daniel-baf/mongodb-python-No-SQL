from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic
from DB import DBDict
import datetime


class MainWindow(QMainWindow):
    searchbar = ''

    def __init__(self):
        super().__init__()

        uic.loadUi("views/resources/main-window.ui", self)
        self.show()

        self.update_student_list()
        self.update_article_list()
        self.update_comment_list()

        self.findStudent.clicked.connect(self.find_student)
        self.insertStudent.clicked.connect(self.insert_student)
        self.updateStudent.clicked.connect(self.update_student)
        self.deleteStudent.clicked.connect(self.delete_student)

        self.findArticle.clicked.connect(self.find_article)
        self.insertArticle.clicked.connect(self.insert_article)
        self.updateArticle.clicked.connect(self.update_article)
        self.deleteArticle.clicked.connect(self.delete_article)

        self.insertComment.clicked.connect(self.insert_comment)

    def update_student(self):
        name = self.name.text()
        user = self.user.text()
        password = self.password.text()
        last_name = self.last_name.text()

        DBDict.update_student({"name": self.searchbar}, {"name": name, "last_name": last_name,
                                                         "user": user, "password": password})

        self.name.clear()
        self.user.clear()
        self.password.clear()
        self.last_name.clear()

        self.update_student_list()

    def update_article(self):
        title = self.title.text()
        article = self.article.toPlainText()

        DBDict.update_article({"title": self.searchbar}, {"title": title, "article": article})

        self.title.clear()
        self.article.clear()

        self.update_student_list()
        self.update_article_list()

    def delete_student(self):
        DBDict.delete_student({"name": self.searchbar})

        self.update_student_list()

        self.last_name.clear()
        self.password.clear()
        self.name.clear()
        self.user.clear()

    def delete_article(self):
        student_id = self.student_id.itemText(self.student_id.currentIndex())
        student_id_auth = self.student_id_auth.itemText(self.student_id_auth.currentIndex())

        DBDict.delete_article({"title": self.searchbar})

        self.searchbar = student_id
        cursor = DBDict.find_students({}, {"name": self.searchbar})

        strings = []
        for document in cursor:
            string = str(document)
            strings.append(string)

        joined_strings = '\n'.join(strings)
        lines = joined_strings.split('\n')

        columns = []
        for line in lines:
            data = line.split(':')

            for dato in data:
                columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

        DBDict.update_student({"name": self.searchbar}, {"no_articles": int(columns[5]) - 1})

        self.searchbar = student_id_auth
        cursor = DBDict.find_students({}, {"name": self.searchbar})

        strings = []
        for document in cursor:
            string = str(document)
            strings.append(string)

        joined_strings = '\n'.join(strings)
        lines = joined_strings.split('\n')

        columns = []
        for line in lines:
            data = line.split(':')

            for dato in data:
                columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

        DBDict.update_student({"name": self.searchbar}, {"no_approves": (int(columns[5]) - 1)})

        self.update_student_list()
        self.update_article_list()

        self.title.clear()
        self.article.clear()

    def find_student(self):
        self.searchbar = self.findStudent_searchbar.text()
        if self.searchbar:
            try:
                cursor = DBDict.find_students({}, {"name": self.searchbar})

                strings = []
                for document in cursor:
                    string = str(document)
                    strings.append(string)

                joined_strings = '\n'.join(strings)
                lines = joined_strings.split('\n')

                columns = []
                for line in lines:
                    data = line.split(':')

                    for dato in data:
                        columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

                self.name.setText(columns[2].replace("'", ''))
                self.user.setText(columns[7].replace("'", ''))
                self.password.setText(columns[8].replace("'", ''))
                self.last_name.setText(columns[3].replace("'", ''))

                self.findStudent_searchbar.clear()

            except Exception as e:
                print(e)

    def find_article(self):
        self.searchbar = self.findArticle_searchbar.text()
        if self.searchbar:
            try:
                cursor = DBDict.find_articles({}, {"title": self.searchbar})

                strings = []
                for document in cursor:
                    string = str(document)
                    strings.append(string)

                joined_strings = '\n'.join(strings)
                lines = joined_strings.split('\n')

                columns = []
                for line in lines:
                    data = line.split(':')

                    for dato in data:
                        columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

                self.title.setText(columns[2].replace("'", ''))
                self.article.setText(columns[3].replace("'", ''))

                item_text = columns[5].replace("'", '')

                for i in range(self.student_id.count()):
                    if self.student_id.itemText(i) == item_text:
                        self.student_id.setCurrentIndex(i)
                        break

                item_text = columns[6].replace("'", '')

                for i in range(self.student_id_auth.count()):
                    if self.student_id_auth.itemText(i) == item_text:
                        self.student_id_auth.setCurrentIndex(i)
                        break

                self.findArticle_searchbar.clear()

            except Exception as e:
                print(e)

    def insert_student(self):
        name = self.name.text()
        user = self.user.text()
        password = self.password.text()
        last_name = self.last_name.text()

        DBDict.insert_student(name, last_name, user, password)

        self.name.clear()
        self.user.clear()
        self.password.clear()
        self.last_name.clear()

        self.update_student_list()

    def insert_article(self):
        title = self.title.text()
        n_date = datetime.datetime.now()
        article = self.article.toPlainText()
        student_id = self.student_id.itemText(self.student_id.currentIndex())
        student_id_auth = self.student_id_auth.itemText(self.student_id_auth.currentIndex())

        DBDict.insert_article(title, article, n_date, student_id, student_id_auth)

        self.searchbar = student_id
        cursor = DBDict.find_students({}, {"name": self.searchbar})

        strings = []
        for document in cursor:
            string = str(document)
            strings.append(string)

        joined_strings = '\n'.join(strings)
        lines = joined_strings.split('\n')

        columns = []
        for line in lines:
            data = line.split(':')

            for dato in data:
                columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

        DBDict.update_student({"name": self.searchbar}, {"no_articles": int(columns[5]) + 1})

        self.searchbar = student_id_auth
        cursor = DBDict.find_students({}, {"name": self.searchbar})

        strings = []
        for document in cursor:
            string = str(document)
            strings.append(string)

        joined_strings = '\n'.join(strings)
        lines = joined_strings.split('\n')

        columns = []
        for line in lines:
            data = line.split(':')

            for dato in data:
                columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

        DBDict.update_student({"name": self.searchbar}, {"no_approves": int(columns[5]) + 1})

        self.title.clear()
        self.article.clear()
        self.student_id.clear()
        self.student_id_auth.clear()

        self.update_article_list()
        self.update_student_list()

    def insert_comment(self):
        n_date = datetime.datetime.now()
        comment = self.comment.toPlainText()
        article = self.article_2.itemText(self.article_2.currentIndex())
        student_id = self.student_id_2.itemText(self.student_id_2.currentIndex())

        DBDict.insert_comment(comment, n_date, student_id, article)

        self.searchbar = student_id
        cursor = DBDict.find_students({}, {"name": self.searchbar})

        strings = []
        for document in cursor:
            string = str(document)
            strings.append(string)

        joined_strings = '\n'.join(strings)
        lines = joined_strings.split('\n')

        columns = []
        for line in lines:
            data = line.split(':')

            for dato in data:
                columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

        DBDict.update_student({"name": self.searchbar}, {"no_comments": int(columns[6]) + 1})

        self.update_student_list()
        self.update_article_list()
        self.update_comment_list()

        self.comment.clear()

    def update_student_list(self):
        try:
            cursor = DBDict.find_students()

            strings = []
            for document in cursor:
                string = str(document)
                strings.append(string)

            joined_strings = '\n'.join(strings)
            lines = joined_strings.split('\n')

            self.student_id.clear()
            self.student_id_2.clear()
            self.student_id_auth.clear()
            self.student_table.setRowCount(0)
            self.student_id.addItem('--Seleccionar--')
            self.student_id_2.addItem('--Seleccionar--')
            self.student_id_auth.addItem('--Seleccionar--')

            for line in lines:
                data = line.split(':')
                columns = []

                for dato in data:
                    columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

                self.student_table.insertRow(self.student_table.rowCount())
                self.student_table.setItem(self.student_table.rowCount() - 1, 0, QTableWidgetItem(columns[2]))
                self.student_table.setItem(self.student_table.rowCount() - 1, 1, QTableWidgetItem(columns[3]))
                self.student_table.setItem(self.student_table.rowCount() - 1, 2, QTableWidgetItem(columns[4]))
                self.student_table.setItem(self.student_table.rowCount() - 1, 3, QTableWidgetItem(columns[5]))
                self.student_table.setItem(self.student_table.rowCount() - 1, 4, QTableWidgetItem(columns[6]))
                self.student_table.setItem(self.student_table.rowCount() - 1, 5, QTableWidgetItem(columns[7]))
                self.student_table.setItem(self.student_table.rowCount() - 1, 6, QTableWidgetItem(columns[8]))

                self.student_id.addItem(columns[2].replace("'", ''))
                self.student_id_2.addItem(columns[2].replace("'", ''))
                self.student_id_auth.addItem(columns[2].replace("'", ''))

            self.student_logs.setText(joined_strings)

        except Exception as e:
            print(e)

    def update_article_list(self):
        try:
            cursor = DBDict.find_articles()

            strings = []
            for document in cursor:
                string = str(document)
                strings.append(string)

            joined_strings = '\n'.join(strings)
            lines = joined_strings.split('\n')

            self.article_2.clear()
            self.article_table.setRowCount(0)
            self.article_2.addItem('--Seleccionar--')

            for line in lines:
                data = line.split(':')
                columns = []

                for dato in data:
                    columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

                self.article_table.insertRow(self.article_table.rowCount())
                self.article_table.setItem(self.article_table.rowCount() - 1, 0, QTableWidgetItem(columns[2]))
                self.article_table.setItem(self.article_table.rowCount() - 1, 1, QTableWidgetItem(columns[3]))
                self.article_table.setItem(self.article_table.rowCount() - 1, 2, QTableWidgetItem(columns[5]))
                self.article_table.setItem(self.article_table.rowCount() - 1, 3, QTableWidgetItem(columns[6]))

                self.article_2.addItem(columns[2].replace("'", ''))

            self.article_logs.setText(joined_strings)

        except Exception as e:
            print(e)

    def update_comment_list(self):
        try:
            cursor = DBDict.find_comments()

            strings = []
            for document in cursor:
                string = str(document)
                strings.append(string)

            joined_strings = '\n'.join(strings)
            lines = joined_strings.split('\n')

            self.comment_table.setRowCount(0)

            for line in lines:
                data = line.split(':')
                columns = []

                for dato in data:
                    columns.append(dato.split(',')[0].split('}')[0].replace(' ', ''))

                self.comment_table.insertRow(self.comment_table.rowCount())
                self.comment_table.setItem(self.comment_table.rowCount() - 1, 0, QTableWidgetItem(columns[2]))
                self.comment_table.setItem(self.comment_table.rowCount() - 1, 2, QTableWidgetItem(columns[5]))
                self.comment_table.setItem(self.comment_table.rowCount() - 1, 1, QTableWidgetItem(columns[4]))

            self.comment_logs.setText(joined_strings)

        except Exception as e:
            print(e)
