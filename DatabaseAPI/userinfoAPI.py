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
def add_user(id,name,location,health,activity):#*args?
    try:
         with connection.cursor() as cursor:
             query=""" INSERT INTO userinfo (userid,username,userlocation,health,activity)
             VALUES (%s,%s,%s,%s,%s)"""
             cursor.execute(query,(id,name,location,health,activity, ))
             connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result


def update_health_status(id,health):#update by id or name
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userino set health=%s WHERE userid= %s """
            cursor.execute(query,(id,health, ))
            connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result

def add_activity(id,activity):#adding another activity
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userino set activity=activity + %s WHERE userid= %s """
            cursor.execute(query,(id,activity, ))
            connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result


def update_location(id,location):#beginning of every sesssion we can ask where he is or getlocation from telegram??
    try:
        with connection.cursor() as cursor:
            query=""" UPDATE userino set location=%s WHERE userid= %s """
            cursor.execute(query,(id,location, ))
            connection.commit()
    except:
        result = "ERROR connecting to DATABASE"
    return result



