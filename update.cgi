#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
import update

<<<<<<< HEAD

def main():
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'wzhang2_db'
=======
def main():
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'twen2_db'
>>>>>>> origin/master
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)
    
    form_data = cgi.FieldStorage()
<<<<<<< HEAD
    env = Environment(loader=FileSystemLoader('./'))
    tmpl = env.get_template('updatePage.html')
=======
    tmpl = cgi_utils_sda.file_contents('updatePage.html')
>>>>>>> origin/master

    display = ""

    if "addRes" in form_data:
        # process the input and add the restaurant
        nameValid = "resName" in form_data
        locaValid = "loca" in form_data
        cuiValid = "cuisine" in form_data
<<<<<<< HEAD
        # typeValid = "resType" in form_data
        if (nameValid and locaValid and cuiValid and typeValid):
=======
        if (nameValid and locaValid and cuiValid):
>>>>>>> origin/master
            display = update.insertRes(conn, form_data)
        else:
            if not nameValid:
                display += "Please enter the restaurant name.\n"
            if not locaValid:
                display += "Please enter the restaurant location.\n"
            if not cuiValid:
                display += "Please enter the cuisine type.\n"
            # if not typeValid:
            #     display += "Please select a restaurant type.\n"
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
<<<<<<< HEAD
    page = tmpl.format(message = display)
    return page
=======
    # page = tmpl.format(message = display)
    return display
>>>>>>> origin/master


if __name__ == '__main__':
    print 'Content-type: text/html\n'
    # displays the webpage
<<<<<<< HEAD
    print main()
=======
    print main()
>>>>>>> origin/master
