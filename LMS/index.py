from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb
import datetime

from PyQt5.uic import loadUiType

ui, _ = loadUiType('mainwindow.ui')
login, _ = loadUiType('login.ui')



class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.handle_login()

        self.pushButton.clicked.connect(self.handle_login)


    def handle_login(self):


        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        user_login_data = self.cur.fetchall()
        for row in user_login_data:
            if username == row[1] and password == row[3]:
                print('User match')
                self.window2 = MainApp()
                self.close()
                self.window2.show()
            else:
                self.label_2.setText('Make sure you entered valid username and password')





class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui_change()
        self.handle_buttons()
        # self.cur = initialize_cursor()
        self.show_category()
        self.show_author()

        self.show_category_combo_box()
        self.show_authors_combo_box()

        self.show_all_client()
        self.show_all_books()

        self.show_all_operation()



############################################
###################Handlebuttons############
    def handle_ui_change(self):
        self.hiding_themes()
        self.tabWidget.tabBar().setVisible(False)


    def handle_buttons(self):
        self.pushButton_5.clicked.connect(self.show_themes)
        self.pushButton_20.clicked.connect(self.hiding_themes)


        self.pushButton.clicked.connect(self.open_user_panel)
        self.pushButton_3.clicked.connect(self.open_books_tab)
        self.pushButton_29.clicked.connect(self.open_client_tab)
        self.pushButton_2.clicked.connect(self.open_users_tab)
        self.pushButton_4.clicked.connect(self.open_settings_tab)


        self.pushButton_7.clicked.connect(self.add_new_books)
        self.pushButton_9.clicked.connect(self.search_books)
        self.pushButton_8.clicked.connect(self.edit_books)
        self.pushButton_10.clicked.connect(self.remove_books)
        self.pushButton_11.clicked.connect(self.add_new_user)



        self.pushButton_14.clicked.connect(self.add_category)
        self.pushButton_15.clicked.connect(self.add_author)

        self.pushButton_12.clicked.connect(self.loging_for_user)
        self.pushButton_13.clicked.connect(self.edit_user)


        self.pushButton_16.clicked.connect(self.dark_blue_theme)
        self.pushButton_17.clicked.connect(self.gray_theme)
        # self.pushButton_18.clicked.connect(self.qdark_theme)
        self.pushButton_19.clicked.connect(self.pstyle_theme)

        self.pushButton_21.clicked.connect(self.add_new_client)
        self.pushButton_23.clicked.connect(self.search_client)
        self.pushButton_24.clicked.connect(self.remove_client)
        self.pushButton_22.clicked.connect(self.edit_client)


        self.pushButton_6.clicked.connect(self.handle_day_op)


    def show_themes(self):
        self.groupBox_3.show()


    def hiding_themes(self):
        self.groupBox_3.hide()


############################################
###################OpeningTabs##############
    def open_user_panel(self):
        self.tabWidget.setCurrentIndex(0)


    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)

    def open_client_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(3)


    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)

#####################################################
##################Day Operations#####################

    def handle_day_op(self):
        book_name = self.lineEdit.text()
        client_name = self.lineEdit_32.text()
        type = self.comboBox.currentText()
        days_number = self.comboBox_2.currentIndex() + 1
        today_date = datetime.date.today()
        to_date = today_date + datetime.timedelta(days=days_number)

        # print(today_date, to_date)


        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO operations(book_name, client, type, days, date, to_date )
            VALUES(%s, %s, %s, %s, %s, %s)
        ''', (book_name, client_name, type, days_number, today_date, to_date))

        self.db.commit()
        self.statusBar().showMessage('New operation added')
        self.show_all_operation()

    def show_all_operation(self):
        self.tableWidget.insertRow(0)

        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_name, client, type, date, to_date  FROM operations ''')

        operation_data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(operation_data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)












############################################
##################Books#####################

    def show_all_books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute((''' SELECT book_name, book_description, book_ID, book_category, book_author, book_availability FROM books'''))
        data_book_all = self.cur.fetchall()

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        for row, form in enumerate(data_book_all):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)

        self.db.close()
    def add_new_books(self):
        self.db = MySQLdb.connect(host='localhost' , user= 'root', password= '*****', db='Library')
        self.cur = self.db.cursor()

        book_name = self.lineEdit_2.text()
        book_description = self.textEdit_2.toPlainText()
        book_ID = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_availability = self.lineEdit_19.text()

        self.cur.execute('''
            INSERT INTO books(book_name, book_description, book_ID, book_category, book_author, book_availability)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (book_name, book_description, book_ID, book_category, book_author, book_availability))

        self.db.commit()
        self.statusBar().showMessage('New book added')

        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_19.setText('')
        self.textEdit_2.setPlainText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.show_all_books()

    def search_books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        book_name = self.lineEdit_4.text()
        sql = ''' SELECT * FROM books WHERE book_name = %s'''

        self.cur.execute(sql, [(book_name)])

        data_search_book = self.cur.fetchone()

        self.lineEdit_6.setText(data_search_book[1])
        self.textEdit.setText(data_search_book[2])
        self.lineEdit_5.setText(data_search_book[3])
        self.comboBox_6.setCurrentText(data_search_book[4])
        self.comboBox_5.setCurrentText(data_search_book[5])
        self.lineEdit_20.setText(str(data_search_book[6]))



    def edit_books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        book_name = self.lineEdit_6.text()
        book_description = self.textEdit.toPlainText()
        book_ID = self.lineEdit_5.text()
        book_category = self.comboBox_6.currentText()
        book_author = self.comboBox_5.currentText()
        book_availability = self.lineEdit_20.text()

        search_book_name = self.lineEdit_4.text()

        self.cur.execute('''
            UPDATE books SET book_name = %s, book_description = %s, book_ID = %s, book_category = %s, book_author = %s, book_availability = %s WHERE book_name = %s 
        ''', (book_name, book_description, book_ID, book_category, book_author, book_availability, search_book_name))
        self.db.commit()

        self.statusBar().showMessage('Book updated')
        self.show_all_books()




    def remove_books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        book_name = self.lineEdit_4.text()

        warning = QMessageBox.warning(self, 'Delete book', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM books WHERE book_name = %s '''
            self.cur.execute(sql, [(book_name)])
            self.db.commit()
            self.statusBar().showMessage('Book removed')
            self.show_all_books()

#############################################
###################Client####################

    def show_all_client(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute((''' SELECT client_name, client_email, client_nid FROM clients'''))
        data_client_all = self.cur.fetchall()

        self.tableWidget_4.setRowCount(0)

        self.tableWidget_4.insertRow(0)
        for row, form in enumerate(data_client_all):
            for column , item in enumerate(form):
                self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                column +=1
            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)
        self.db.close()


    def add_new_client(self):
        client_name = self.lineEdit_21.text()
        client_email = self.lineEdit_22.text()
        client_nid = self.lineEdit_23.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO clients(client_name, client_email, client_nid)
            VALUES (%s, %s, %s)
        ''', (client_name, client_email, client_nid))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New client added')
        self.show_all_client()




    def search_client(self):
        client_nid = self.lineEdit_24.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        sql = ''' SELECT * FROM clients WHERE client_nid = %s'''
        self.cur.execute(sql, [(client_nid)])
        data_client_nid = self.cur.fetchone()
        print(data_client_nid)

        self.lineEdit_31.setText(data_client_nid[1])
        self.lineEdit_29.setText(data_client_nid[2])
        self.lineEdit_30.setText(data_client_nid[3])

    def edit_client(self):
        client_original_nid = self.lineEdit_24.text()
        client_name = self.lineEdit_31.text()
        client_email = self.lineEdit_29.text()
        client_nid = self.lineEdit_30.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            UPDATE clients SET client_name = %s, client_email = %s, client_nid = %s WHERE client_nid = %s
        ''', (client_name, client_email, client_nid, client_original_nid))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Client information updated')

        self.show_all_client()


    def remove_client(self):
        client_original_nid = self.lineEdit_24.text()

        warning_message = QMessageBox.warning(self, "delete Client", "Are you sure?", QMessageBox.Yes | QMessageBox.No)

        if warning_message == QMessageBox.Yes:
            self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
            self.cur = self.db.cursor()

            sql = ''' DELETE FROM clients WHERE client_nid =%s '''
            self.cur.execute(sql, [(client_original_nid)])

            self.db.commit()
            self.db.close()
            self.statusBar().showMessage('Client removed')
            self.show_all_client()




############################################
###################Users####################
    def add_new_user(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()


        username = self.lineEdit_7.text()
        email = self.lineEdit_8.text()
        password = self.lineEdit_9.text()
        re_password = self.lineEdit_10.text()

        if password == re_password:
            self.cur.execute('''
                INSERT INTO users(user_name, user_email, user_password)
                VALUES (%s, %s, %s)
            ''', (username, email, password))

            self.db.commit()
            self.statusBar().showMessage('User added')
            self.label_30.setText('')
        else:
            self.label_30.setText('Password did not match')

    def loging_for_user(self):
        username = self.lineEdit_12.text()
        password = self.lineEdit_11.text()

        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        user_login_data = self.cur.fetchall()
        for row in user_login_data:
            if username == row[1] and password ==row[3]:
                print('User match')
                self.statusBar().showMessage('Valid username and password')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_16.setText(row[1])
                self.lineEdit_13.setText(row[2])
                self.lineEdit_14.setText(row[3])
            else:
            #     self.groupBox_4.setEnabled(False)
                self.statusBar().showMessage('Invalid username and password')


    def edit_user(self):
        username = self.lineEdit_16.text()
        email = self.lineEdit_13.text()
        password = self.lineEdit_14.text()
        re_password = self.lineEdit_15.text()

        previous_username = self.lineEdit_12.text()

        if password == re_password:
            self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
            self.cur = self.db.cursor()


            self.cur.execute('''
                UPDATE users SET user_name = %s, user_email = %s, user_password = %s WHERE user_name = %s
            ''', (username, email, password, previous_username))

            self.db.commit()
            self.statusBar().showMessage('User information updated successfully')
            # self.label_30.setText('')
        else:
            self.label_30.setText('Password did not match')



############################################
###################Settings#################


    def add_category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()


        category_name = self.lineEdit_17.text()
        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
            ''', (category_name,))
        self.db.commit()
        self.statusBar().showMessage('New category added')
        self.lineEdit_17.setText('')
        self.show_category()
        self.show_category_combo_box()



    def show_category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category''')
        data_category = self.cur.fetchall()

        # print(data_category)
        if data_category:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data_category):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column+=1
                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)


    def add_author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_18.text()
        self.cur.execute('''
                    INSERT INTO authors (author_name) VALUES (%s)
                    ''', (author_name,))
        self.db.commit()
        self.statusBar().showMessage('New author added')
        self.lineEdit_18.setText('')
        self.show_author()
        self.show_authors_combo_box()


    def show_author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors''')
        data_author = self.cur.fetchall()

        # print(data_author)
        if data_author:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data_author):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1
                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)



#########################################################
###################Show settings data in UI##############


    def show_category_combo_box(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute( ''' SELECT category_name FROM category''' )
        data_category_combo = self.cur.fetchall()
        self.comboBox_3.clear()
        for category in data_category_combo:
            self.comboBox_3.addItem(category[0])
            self.comboBox_6.addItem(category[0])

    def show_authors_combo_box(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='*****', db='Library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors''')
        data_author_combo = self.cur.fetchall()
        self.comboBox_4.clear()
        for author in data_author_combo:
            self.comboBox_4.addItem(author[0])
            self.comboBox_5.addItem(author[0])


############################################
###################UITheme#################
    def dark_blue_theme(self):
        with open('Themes/darkblue.css', 'r') as file:
            style_sheet = file.read()
            self.setStyleSheet(style_sheet)
        # style = open('Themes/darkblue.css', 'r')
        # style.read()
        # self.setStyleSheet(style)


    def gray_theme(self):
        with open('Themes/gray.css', 'r') as file:
            style_sheet = file.read()
            self.setStyleSheet(style_sheet)
        # style = open('Themes/gray.css', 'r')
        # style.read()
        # self.setStyleSheet(style)


    def pstyle_theme(self):
        with open('Themes/pstyle.css', 'r') as file:
            style_sheet = file.read()
            self.setStyleSheet(style_sheet)
        # style = open('Themes/pstyle.css', 'r')
        # style.read()
        # self.setStyleSheet(style)


    # def qdark_theme(self):
    #     with open('Themes/qdark.css', 'r') as file:
    #         style_sheet = file.read()
    #         self.setStyleSheet(style_sheet)
    #     # style = open('Themes/qdark.css', 'r')
    #     # style.read()
    #     # self.setStyleSheet(style)





def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
