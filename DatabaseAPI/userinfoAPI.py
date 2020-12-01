import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    db="questions",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


#ADDING NEW USER
def add_user(id,name,location,health,q_counter):#*args?
    try:
         with connection.cursor() as cursor:
             query=""" INSERT INTO userinfo (userid,username,userlocation,health,quest_counter)
             VALUES (%s,%s,%s,%s,%s)"""
             cursor.execute(query,(id,name,location,health,q_counter, ))
             connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result


def update_health_status(id,health):#update by id or name
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userinfo set health=%s WHERE userid= %s """
            cursor.execute(query,(id,health, ))
            connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result


def update_location(id,location):#beginning of every sesssion we can ask where he is or getlocation from telegram??
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userinfo set location=%s WHERE userid= %s """
            cursor.execute(query,(id,location, ))
            connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result

def add_activity(userid,activity):#adding another activity
    try:
        with connection.cursor() as cursor:
            query=""" INSERT INTO activities (userid,activity) VALUES(%s,%s)"""
            cursor.execute(query,(userid,activity, ))
            connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result

def fetch_activity(userid):#adding another activity
    try:
        with connection.cursor() as cursor:
            query=""" SELECT activity FROM activities WHERE userid=%s ORDER BY RAND() LIMIT 1"""
            cursor.execute(query,(userid,activity, ))
            result=cursor.fetchone()
    except:
        result = "ERROR connecting to DATABASE"
    return result

def update_question_counter(userid, q_counter):
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userinfo set quest_counter=%s WHERE userid=%s """
            cursor.execute(query,(q_counter,userid, ))
            connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result

