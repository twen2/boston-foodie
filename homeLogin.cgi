#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
import Cookie
import login
from jinja2 import Environment, FileSystemLoader

# this is the cgi file for login in home page
def main():
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'wzhang2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)

    form_data = cgi.FieldStorage()

    loggedInTop = '''<h2>{{username}} Welcome Login!
            <br><b>Explore</b> the restaurants and satisfy your taste
            <br><b>Add</b> new restaurants or dishes
            <br><b>Like</b> dishes and <b>Comment</b> restaurants</h2>'''
    loggedInChoices = '''<ul>
                            <li><a href="genSearch.cgi"><span id = "mainName">General Search</span>
                                <br><br>Search for an ideal restaurant based on location and type</a>

                            <li><a href="dishSearch.cgi"><span id = "mainName">Dishes Search</span>
                                <br><br>Search for an ideal restaurant based on your favorite dish</a>
                             
                            <li><a href="updatepage.cgi"><span id = "mainName">Update Database</span>
                                <br><br>Update the database through adding, liking and commenting</a>
                         </ul>'''
    loggedInForm = '''<form id="logout" method=POST action="homeLogin.cgi" style="text-indent: 10px">
                    <input type="submit" name="logout" value="Logout"></form>'''

    generalTop = '''<span id = "mainName">Login Page</span><br><p><i>Login to explore more!</i><br>'''
    generalChoices = '''<ul><li><a href="home.cgi"><span id = "mainName">Back to Home Page</span></ul>'''
    generalForm = '''<form id="login" method=POST action="homeLogin.cgi">
           <p>Username: <input type=text name="username">
           <p>Password: <input type=password name="password"><br></br>
           <input type="submit" name="login" value="Login">
           <input type="submit" name="register" value="Register"></form>'''

    display = ""

    env = Environment(loader=FileSystemLoader('./'))
    tmpl = env.get_template('homepageLogin.html')

    oreo = cgi_utils_sda.getCookieFromRequest('user')
    if oreo != None:
        user = oreo.value
    else:
        user = ""

    # if the user submitted the login form
    # if "login" in form_data:
    if ("login" in form_data or "register" in form_data):
        if not ("username" in form_data and "password" in form_data):
            display = "Please enter a valid username and password.\n"
            return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)
        else:
          username = form_data.getfirst("username")
          password = form_data.getfirst("password")
        
          if 'login' in form_data:
              result = login.verify(conn, username, password)
            # loggedIn = result[0]
            # display = result[1]

          if 'register' in form_data:
              result = login.register(conn, username, password)

          loggedIn = result[0]
          display = result[1]
        
        if loggedIn:
            user = username
            oreo = Cookie.SimpleCookie()
            cgi_utils_sda.setCookie(oreo, 'user', user)
            cgi_utils_sda.print_headers(oreo)
            return tmpl.render(top = loggedInTop, choices = loggedInChoices, form = loggedInForm, result = display)
        else:
            cgi_utils_sda.print_headers(None)
            return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)

    if 'logout' in form_data:
        print 'logout'
        oreo = Cookie.SimpleCookie()
        cgi_utils_sda.setCookie(oreo, 'user', value='', expires=0)
        cgi_utils_sda.print_headers(oreo)
        return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)

    if user != '':
        oreo = Cookie.SimpleCookie()
        cgi_utils_sda.setCookie(oreo, 'user', user)
        cgi_utils_sda.print_headers(oreo)
        display = "Logged in as " + user
        return tmpl.render(top = loggedInTop, choices = loggedInChoices, form = loggedInForm,result = display)
    else:
        cgi_utils_sda.print_headers(None)
        return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()
