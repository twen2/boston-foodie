#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader
import update

# this is the cgi for the update page, user can either add restaurants or add dishes
def main():
    oreo = cgi_utils_sda.getCookieFromRequest('user')
    # print oreo.value
    userInfo = ""
    logoutForm = ""
    if oreo != None:
        user = oreo.value
        userInfo = "Logged in as " + user
        logoutForm = '''<form id="logout" method=POST action="homeLogin.cgi" style="text-indent: 10px">
                    <input type="submit" name="logout" value="Logout"></form>'''
    else:
        tmpl = env.get_template('homepageLogin.html')
        generalTop = '''<span id = "mainName">Login Page</span><br><p><i>Login to explore more!</i><br>'''
        generalChoices = '''<ul><li><a href="home.cgi"><span id = "mainName">Back to Home Page</span></ul>'''
        generalForm = '''<form id="login" method=POST action="homeLogin.cgi">
               <p>Username: <input type=text name="username">
               <p>Password: <input type=password name="password"><br></br>
               <input type="submit" name="login" value="Login">
               <input type="submit" name="register" value="Register"></form>'''
        display = "Please login before contribute, thank you!"
        return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)

    # connect to database
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'twen2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)
    
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

    page = tmpl.render(message = display, defaultResName=restName, userInfo = userInfo, form = logoutForm)
    return page


if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print main()

