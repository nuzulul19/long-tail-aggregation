import mysql.connector as sql
import settings


class Db():
    def __init__(self):
        self.conn = sql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_DATABASE,
        )

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()
