#!/usr/local/bin/python2.7


import sys 
import cgi
import cgitb; cgitb.enable()
import dbconn2
import MySQLdb

def verify(conn, username, password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT count(*) AS n FROM users WHERE username = %s AND password = %s', (username, password))
    row = curs.fetchone()
    if row['n'] == 0:
        return False, "Incorrect username or password. Please try again or register with a new username."
    else:
        curs.execute('SELECT id FROM users WHERE username = %s AND password = %s', (username, password))
        idrow = curs.fetchone()
        return True, "Logged in as " + username, idrow['id']

def register(conn, username, password):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT count(*) AS n FROM users WHERE username = %s', (username))
    row = curs.fetchone()
    if row['n'] != 0:
        return False, "Sorry, the username already exists. Please register with another username again."
    else:
        curs.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        curs.execute('SELECT id FROM users WHERE username = %s AND password = %s', (username, password))
        idrow = curs.fetchone()
        return True, "Successfully registered and logged in as " + username, idrow['id']

# # though the username is unique, which check password as well in case
# def getID(conn, username):
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('SELECT id FROM users WHERE username = %s AND password = %s', (username, password))