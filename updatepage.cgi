#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader
import update
import search

# this is the cgi for the update page, user can either add restaurants or add dishes
def main():
    # connect to database
    conn = search.init()
    
    form_data = cgi.FieldStorage()
    # set up env and get template
    env = Environment(loader=FileSystemLoader('./'))
    tmpl = env.get_template('updatePage.html')


    display = ""
    restName = ""
    # in the case the add restaurant form is submitted
    if "addRest" in form_data:
        # process the input and add the restaurant
        nameValid = "resName" in form_data
        locaValid = "loca" in form_data
        cuiValid = "cuisine" in form_data
        # only all three is enter will the form be submitted successfully
        if (nameValid and locaValid and cuiValid):
            restName = form_data.getfirst("resName")
            display = update.insertRes(conn, form_data)
        else:
            # otherwise, error message will be displayed
            if not nameValid:
                display += 'Please enter the restaurant name.\n'
            if not locaValid:
                display += 'Please enter the restaurant location.\n'
            if not cuiValid:
                display += 'Please enter the cuisine type.\n'

    # in the case the add dish form is submitted
    elif "addDishes" in form_data:
        dishValid = "dishName" in form_data
        resValid = "res" in form_data
        # only both dish and restaurant being entered will the form be submitted successfully
        if dishValid and resValid:
            # update the database through insertDish function
            display = update.insertDish(conn, form_data)
        else:
            # otherwise, error message will be displayed, telling user what is missing
            if not dishValid:
                display += 'Please enter the dish name.\n'
            if not resValid:
                display += 'Please enter the restaurant name.\n'
    # in the case nothing is happen to the page, the page will stay in original status with no message or result displayed
    else:
        display = ""

    page = tmpl.render(message = display, defaultResName=restName)
    return page


if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print main()

