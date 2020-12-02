import pymysql
from config import DB, DB_password

connection = pymysql.connect(
    host="localhost",
    user="root",
    password=DB_password,
    db=DB,
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def add_feedBack(userid,feedBack):#adding another feedBack
    try:
        with connection.cursor() as cursor:
            query=""" INSERT INTO feedBack (userid,feedBack) VALUES(%s,%s)"""
            cursor.execute(query,(userid,feedBack, ))
            connection.commit()
    except:
        return "ERROR connecting to DATABASE"