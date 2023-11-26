# import logging
# import os
# import sqlite3 as sqlite
#
#
# class Store:
#     database: str
#
#     def __init__(self, db_path):
#         self.database = os.path.join(db_path, "be.db")
#         self.init_tables()
#
#     def init_tables(self):
#         try:
#             conn = self.get_db_conn()
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS user ("
#                 "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
#                 "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS user_store("
#                 "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS store( "
#                 "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
#                 " PRIMARY KEY(store_id, book_id))"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order( "
#                 "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
#             )
#
#             conn.execute(
#                 "CREATE TABLE IF NOT EXISTS new_order_detail( "
#                 "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
#                 "PRIMARY KEY(order_id, book_id))"
#             )
#
#             conn.commit()
#         except sqlite.Error as e:
#             logging.error(e)
#             conn.rollback()
#
#     def get_db_conn(self) -> sqlite.Connection:
#         return sqlite.connect(self.database)
#
#
# database_instance: Store = None
#
#
# def init_database(db_path):
#     global database_instance
#     database_instance = Store(db_path)
#
#
# def get_db_conn():
#     global database_instance
#     return database_instance.get_db_conn()

import logging
import os
import mysql.connector


class Store:
    database: str

    def __init__(self):
        self.database = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='TANGxiaohui0722',
            database='bookstore'
        )
        self.init_tables()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
            cursor = conn.cursor()

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id VARCHAR(255) PRIMARY KEY, password VARCHAR(255) NOT NULL, "
                "balance INTEGER NOT NULL, token VARCHAR(255), terminal VARCHAR(255));"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id VARCHAR(255), store_id VARCHAR(255), PRIMARY KEY(user_id, store_id));"
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS store(
                    store_id VARCHAR(255),
                    book_id VARCHAR(255),
                    tags VARCHAR(255),
                    book_info TEXT,
                    pictures BLOB,
                    id VARCHAR(255),
                    title VARCHAR(255),
                    author VARCHAR(255),
                    publisher VARCHAR(255),
                    original_title VARCHAR(255),
                    translator VARCHAR(255),
                    pub_year VARCHAR(255),
                    pages INTEGER,
                    price INTEGER,
                    binding VARCHAR(255),
                    isbn VARCHAR(255),
                    author_intro VARCHAR(255),
                    book_intro VARCHAR(255),
                    content TEXT,
                    stock_level INTEGER,
                    PRIMARY KEY (store_id, book_id)
                    )
                """
            )

            # cursor.execute(
            #     "CREATE TABLE IF NOT EXISTS new_order( "
            #     "order_id VARCHAR(255) PRIMARY KEY, store_id VARCHAR(255), user_id VARCHAR(255), "
            # )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS new_order ("
                "order_id VARCHAR(255) PRIMARY KEY, "
                "store_id VARCHAR(255), "
                "user_id VARCHAR(255), "
                "book_status INTEGER, "
                "order_time DATETIME)"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id VARCHAR(255), book_id VARCHAR(255), count INTEGER, price INTEGER,  "
                "PRIMARY KEY(order_id, book_id))"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS books( "
                "id VARCHAR(255) PRIMARY KEY,"
                "title VARCHAR(255),"
                "author VARCHAR(255),"
                "publisher VARCHAR(255),"
                "original_title VARCHAR(255),"
                "translator VARCHAR(255),"
                "pub_year VARCHAR(255),"
                "pages VARCHAR(255),"
                "price VARCHAR(255),"
                "binding VARCHAR(255),"
                "isbn VARCHAR(255),"
                "author_intro TEXT,"
                "book_intro TEXT,"
                "content TEXT,"
                "tags VARCHAR(255),"
                "picture BLOB)"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS new_order_paid( "
                "order_id VARCHAR(255), store_id VARCHAR(255), user_id VARCHAR(255), "
                "book_status INTEGER, price INTEGER, "
                "PRIMARY KEY(order_id, user_id))"
            )

            conn.commit()
        except mysql.connector.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> mysql.connector.connection.MySQLConnection:
        return self.database


database_instance = Store()

def init_database():
    global database_instance
    database_instance = Store()

def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
