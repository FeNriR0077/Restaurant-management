import mysql.connector


class MyDB:
    def __init__(self):
        self.my_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="resturant"
        )
        self.my_cursor = self.my_connection.cursor()
        # self.qry = "CREATE DATABASE resturant"
        # self.qry = """CREATE TABLE items (id int PRIMARY KEY AUTO_INCREMENT, name varchar(100),
        #               type varchar(100), price double)"""
        # self.my_cursor.execute(self.qry)

    def iud(self, qry, values):
        try:
            self.my_cursor.execute(qry, values)
            self.my_connection.commit()
            return True
        except Exception:
            return False

    def return_id(self, qry, values):
        try:
            self.my_cursor.execute(qry, values)
            self.my_connection.commit()
            return self.my_cursor.lastrowid
        except Exception:
            return False

    def show_data(self, qry):
        try:
            self.my_cursor.execute(qry)
            data = self.my_cursor.fetchall()
            return data
        except Exception:
            return False

    def show_data_p(self, qry, values):
        try:
            self.my_cursor.execute(qry, values)
            data = self.my_cursor.fetchall()
            return data
        except Exception:
            return False

