#!/usr/local/bin/python2.7


import sys 
import cgi
import cgitb; cgitb.enable()
# import cgi_utils_sda
import dbconn2
import MySQLdb

# This is the file for updating the database based on user's input

# get the id of the restaurant name input, or return -1 if no such restaurant exists
def getRes(conn,resName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM restaurants WHERE name = %s', (resName))
    row = curs.fetchone()
    if curs.rowcount != 0:
        return row["id"]
    else:
        return -1 # we use -1 to keep the output type consistent 

# def getResLoca(conn,resName,loca):
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('SELECT * FROM restaurants WHERE name = %s AND location = %s', (resName,loca))
#     row = curs.fetchone()
#     if curs.rowcount != 0:
#         return row["id"]
#     else:
#         return -1

# insert the input data to the database 
def insertRes(conn, form_data):
    # creates the cursor as dictionary and stores the result set in the client
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    name = cgi.escape(form_data.getfirst("resName")) # avoid xss attack by using escape
    # loca = form_data.getfirst("loca")
    # if getResLoca(conn, name,loca) == -1:

    # if the restaurant doesn't exist, we will insert the new data into database
    if getRes(conn, name) == -1:
        loca = form_data.getfirst("loca")
        cuisine = form_data.getfirst("cuisine")
        resType = form_data.getfirst("resType")
        # the default value of resType is both
        if resType == "":
            resType = "both"

        # executes the given query that inserts the provided data into the table
        curs.execute("""INSERT INTO restaurants(id, name, location, cuisine_type, res_type) VALUES (NULL, %s, %s, %s, %s)""",
                    (name, loca, cuisine, resType))
        
        return "The restaurant " + name + " is successfully inserted."
        # executed the given query that returns the entry that matches the new insertion

    else:
        # if exist, no insertion is allowed
        return "The restaurant " + name + " already exists."

# insert a dish to the database
def insertDish(conn, form_data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    dish = cgi.escape(form_data.getfirst("dishName"))
    resName = cgi.escape(form_data.getfirst("res"))
    resID = getRes(conn, resName) # retrieve the id of the restaurant from the name
    # here we assume no branch exists, so the restaurant name is as unique as its id

    if resID == -1:
        return "Restaurant does not exist."
    else:
        # check if the dish already exist in the restaurant, if not, then insert and notify the user
        if not existDish(conn, resID, dish):
            curs.execute("""INSERT INTO dishes(id, name, num_of_likes, res_id) VALUES (NULL, %s, %s, %s)""",
                        (dish, 0, resID))
            return "The dish " + dish + " is successfully inserted."
        else:
            return "The dish " + dish + " already exists for the restaurant " + resName + "."

# def main(dishID):
#     dsn = dbconn2.read_cnf(".my.cnf")
#     dsn['db'] = 'twen2_db'
#     dsn['host'] = 'localhost'
#     conn = dbconn2.connect(dsn)
#     conn.autocommit(True)
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('''UPDATE dishes SET num_of_likes = %s WHERE id = %s''', (like, dishID))
#     return

if __name__ == "__main__":
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'twen2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)
    data = cgi.FieldStorage()
    dishID = data.getfirst('dishID')
    dishLike = data.getfirst('dishLike')
    imcrementLike(conn, dishID, dishLike)

# update the number of like for each dish after user click the like button
def incrementLike(conn, dishID, userID, like):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('''UPDATE dishes SET num_of_likes = %s WHERE id = %s''', (like, dishID))
    curs.execute('''INSERT INTO likes(user_id,dish_id) VALUES (%s, %s)''', (userID, dishID))

# check if certain dish exists in the restaurant or not
def existDish(conn, resID, dishName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    curs.execute("""SELECT * FROM dishes WHERE res_id = %s AND name = %s""", (resID, dishName))
    return curs.rowcount != 0

def ifRepeatLike(conn, userID, dishID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM likes WHERE user_id = %s AND dish_id = %s', (userID, dishID))
    return curs.rowcount != 0
