#!/usr/local/bin/python2.7


import sys 
import cgi
import cgitb; cgitb.enable()
# import cgi_utils_sda
import dbconn2
import MySQLdb

def getRes(conn,resName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM restaurants WHERE name = %s', (resName))
    row = curs.fetchone()
    if curs.rowcount != 0:
        return row["id"]
    else:
        return -1

def insertRes(conn, form_data):
    # creates the cursor as dictionary and stores the result set in the client
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    name = form_data.getfirst("resName")
    loca = form_data.getfirst("loca")
    cuisine = form_data.getfirst("cuisine")
    resType = form_data.getfirst("resType")

    # executes the given query that inserts the provided data into the table
    curs.execute("""INSERT INTO restaurants(id, name, location, cuisine_type, res_type) VALUES (NULL, %s, %s, %s, %s)""",
                (name, loca, cuisine, resType))
    
    return "The restaurant " + name + " is successfully inserted."
    # executed the given query that returns the entry that matches the new insertion
    # this query is used to check if the actor is inserted succesfully
    # curs.execute('SELECT * FROM movie WHERE tt = %s', (tt))

def insertDish(conn, form_data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    dish = form_data.getfirst("dishName")
    resName = form_data.getfirst("res")
    resID = getRes(conn, resName)
    if resID == -1:
        return "Restaurant does not exist."
    else:
        curs.execute("""INSERT INTO dishes(id, name, num_of_likes, res_id) VALUES (NULL, %s, %s, %s)""",
                    (dish, 0, resID))
        return "The dish " + dish + " is successfully inserted."

