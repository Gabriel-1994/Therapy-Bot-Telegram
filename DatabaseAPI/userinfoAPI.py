import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="sql_intro",
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
        return "ERROR connecting to DATABASE"

def search_user(user_id):#*args?
    try:
         with connection.cursor() as cursor:
             query=""" SELECT * FROM userinfo WHERE userid = %s"""
             cursor.execute(query,(user_id, ))
             connection.commit()
             result=cursor.fetchone()
             if result:
                 return True
             else:
                 return False
    except:
        result = "ERROR connecting to DATABASE"
    return result


def update_health_status(user_id,health):#update by id or name
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userinfo set health=%s WHERE userid=%s """
            cursor.execute(query,(health,user_id, ))
            connection.commit()
    except:
        return "ERROR connecting to DATABASE"

def fetch_health_status(userid):#adding another activity
    try:
        with connection.cursor() as cursor:
            query=""" SELECT health FROM userinfo WHERE userid=%s"""
            cursor.execute(query,(userid, ))
            result=cursor.fetchone()
    except:
        result = "ERROR connecting to DATABASE"
    return float(result.get('health'))


def update_location(user_id,location):#beginning of every sesssion we can ask where he is or getlocation from telegram??
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userinfo set location=%s WHERE userid= %s """
            cursor.execute(query,(user_id,location, ))
            connection.commit()
    except:
       return "ERROR connecting to DATABASE"

def add_activity(userid,activity):#adding another activity
    try:
        with connection.cursor() as cursor:
            query=""" INSERT INTO activities (userid,activity) VALUES(%s,%s)"""
            cursor.execute(query,(userid,activity, ))
            connection.commit()
    except:
        return "ERROR connecting to DATABASE"

def fetch_activity(userid):#adding another activity
    try:
        with connection.cursor() as cursor:
            query=""" SELECT activity FROM activities WHERE userid=%s ORDER BY RAND() LIMIT 1"""
            cursor.execute(query,(userid, ))
            result=cursor.fetchone()
    except:
        result = "ERROR connecting to DATABASE"
    return result

def fetch_Qcounter(userid):#adding another activity
    try:
        with connection.cursor() as cursor:
            query=""" SELECT quest_counter FROM userinfo WHERE userid=%s """
            cursor.execute(query,(userid, ))
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
        return "ERROR connecting to DATABASE"
