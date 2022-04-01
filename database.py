import sqlite3


def initdatabase():
    connection = sqlite3.connect('members.db')

    cursor = connection.cursor()


    command1 = """CREATE  TABLE IF NOT EXISTS
    activity(memberID INTEGER PRIMARY KEY, msg_count INTEGER, Voice_activity INTEGER)"""

    cursor.execute(command1)

def addmessage(id):
    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM 'activity' WHERE memberID = {id}")

    check = cursor.fetchone()


    if(check == None):
        cursor.execute(f"INSERT OR IGNORE INTO activity VALUES ({id},1,0)")
    else:
        cursor.execute(f"UPDATE activity SET msg_count = msg_count + 1 WHERE memberID = {id}")

    connection.commit()

def addvoice(id,count):
    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM 'activity' WHERE memberID = {id}")

    check = cursor.fetchone()


    if(check == None):
        cursor.execute(f"INSERT OR IGNORE INTO activity VALUES ({id},0,{count})")
    else:
        cursor.execute(f"UPDATE activity SET Voice_activity = Voice_activity + {count} WHERE memberID = {id}")

    connection.commit()

def getvoicecount(id):
    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM 'activity' WHERE memberID = {id}")
    check = cursor.fetchone()
    #print(check)
    if(check != None):
        cursor.execute(f"SELECT Voice_activity FROM 'activity' WHERE memberID = {id}")
        count = cursor.fetchone()[0]
    else:
        return 0

    return count

def getmsgcount(id):
    connection = sqlite3.connect('members.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM 'activity' WHERE memberID = {id}")
    check = cursor.fetchone()
    #print(check)
    if(check != None):
        cursor.execute(f"SELECT msg_count FROM 'activity' WHERE memberID = {id}")
        count = cursor.fetchone()[0]
    else:
        return 0

    return count

