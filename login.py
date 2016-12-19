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
    return True, "Logged in as " + username