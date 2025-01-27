import sqlite3
from venv import logger

class Database:
    def __init__(self, path_to_db='main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None,
                fetch_one=False, fetch_all=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetch_one:
            data = cursor.fetchone()
        if fetch_all:
            data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])

    def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                telegram_id BIGINT NOT NULL UNIQUE,
                referal INTEGER
                )
        """
        return self.execute(sql, commit=True)

    def select_one_users(self, telegram_id):
        sql = """
            SELECT * FROM users WHERE telegram_id = ?
        """
        return self.execute(sql, (telegram_id,), fetch_one=True)

    def select_all_users(self):
        sql = "SELECT * FROM users"
        return  self.execute(sql, fetch_all=True)

    def select_all_users1(self,page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
        SELECT * FROM users
        ORDER BY referal DESC
        LIMIT ? OFFSET ?
        """
        return  self.execute(sql,(page_size, offset), fetch_all=True)

    def select_count_users(self):
        sql = "SELECT count(*) FROM users"
        return self.execute(sql, fetch_one=True)

    def add_users(self, fullname:str, telegram_id: int, referal):
        sql = "INSERT INTO users (fullname, telegram_id, referal) VALUES (?, ?, ?)"
        return self.execute(sql, (fullname, telegram_id, referal), commit=True)

    def updete_users(self, old_tg_id, new_tg_id):
        sql = """UPDATE users SET telegram_id = ? WHERE telegram_id = ?"""
        return self.execute(sql, (new_tg_id, old_tg_id), commit=True)
    def add_users_referal(self, tg_id, number):
        sql = """UPDATE users SET referal = ? WHERE telegram_id = ?"""
        return self.execute(sql, (number, tg_id), commit=True)

    def updete_users_referal_clear(self):
        sql = """UPDATE users SET referal = 0"""
        return self.execute(sql, commit=True)

    def create_table_kanal(self):
        sql = """
            CREATE TABLE IF NOT EXISTS kanal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kanal_link TEXT NOT NULL
            )
        """
        return self.execute(sql, commit=True)
    def count_kanal(self):
        sql = "SELECT count(*) FROM kanal"
        return self.execute(sql, fetch_one=True)
    def add_k(self, kanal_nomi):
        sql = """INSERT INTO kanal (kanal_link) VALUES (?)"""
        self.execute(sql, (kanal_nomi, ), commit=True)

    def select_k(self):
        sql = """SELECT kanal_link FROM kanal"""
        return self.execute(sql,fetch_all=True)
    def select_all_kanal1(self,page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  kanal_link FROM kanal
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (page_size,offset), fetch_all=True)

    def delete_k(self,kanal_nomi):
        sql = """DELETE FROM kanal WHERE kanal_link=?"""
        return self.execute(sql, (kanal_nomi,), commit=True)
