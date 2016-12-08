#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader
import update


def main():
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'twen2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)
    
    form_data = cgi.FieldStorage()

    env = Environment(loader=FileSystemLoader('./'))
    tmpl = env.get_template('updatePage.html')


    display = ""
    if "addRes" in form_data:
        # process the input and add the restaurant
        nameValid = "resName" in form_data
        locaValid = "loca" in form_data
        cuiValid = "cuisine" in form_data
        if (nameValid and locaValid and cuiValid):
            display = update.insertRes(conn, form_data)
        else:
            if not nameValid:
                display += "Please enter the restaurant name.\n"
            if not locaValid:
                display += "Please enter the restaurant location.\n"
            if not cuiValid:
                display += "Please enter the cuisine type.\n"

    elif "addDishes" in form_data:
        dishValid = "dishName" in form_data
        resValid = "res" in form_data
        if dishValid and resValid:
            display = update.insertDish(conn, form_data)
        else:
            if not dishValid:
                display += "Please enter the dish name.\n"
            if not resValid:
                display += "Please enter the restaurant name.\n"
    else:
        display = ""

    page = tmpl.render(message = display)
    return page


if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print main()

