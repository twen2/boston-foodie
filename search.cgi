#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
import search

def main():
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'wzhang2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)
    
    form_data = cgi.FieldStorage()

    display = ""
    if ("generalS" in form_data):
        display = search.generalS(conn, form_data)
    elif ("dishS" in form_data):
        if "dish" in form_data:
            display = search.dishS(conn, form_data)
        else:
            display += "Please enter the dish name."
    else:
        display = ""

    return display


if __name__ == '__main__':
    print 'Content-type: text/html\n'
    # displays the webpage
    print main()
