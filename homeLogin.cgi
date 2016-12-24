#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable
import cgi_utils_sda
import dbconn2
import MySQLdb
import Cookie
import login
import json
from jinja2 import Environment, FileSystemLoader

my_sess_dir = '/students/wzhang2/public_html/cgi-bin/beta/session/'
# my_sess_dir = '/students/twen2/public_html/cgi-bin/session/'

# this is the cgi file for login in home page
def main():
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'wzhang2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)

    form_data = cgi.FieldStorage()

    loggedInTop = '''<h2>Welcome Login! <span style ="color:salmon">{username}</span>
            <br><b>Add</b> new restaurants or dishes
            <br><b>Like</b> dishes in various restaurants</h2>'''
    loggedInChoices = '''<ul>
                            <li><a href="genSearch.cgi"><span id = "mainName">General Search</span>
                                <br><br>Search for an ideal restaurant based on location and type</a>

                            <li><a href="dishSearch.cgi"><span id = "mainName">Dish Search</span>
                                <br><br>Search for an ideal restaurant based on your favorite dish</a>
                            <li><a href="lookRes.cgi"><span id = "mainName">Look into Restaurant</span>
                                <br><br>Learn more about specific restaurants</a>
                             
                            <li><a href="updatepage.cgi"><span id = "mainName">Update Database</span>
                                <br><br>Update the database through adding, liking and commenting</a>
                         </ul>'''
    loggedInForm = '''<form id="logoutx method=POST action="homeLogin.cgi" style="text-align:center">
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

    # if the user submitted the login form
    # if "login" in form_data:
    if ("login" in form_data or "register" in form_data):
        if not ("username" in form_data and "password" in form_data):
            display = "Please enter a valid username and password.\n"
            return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)
        else:
          username = cgi.escape(form_data.getfirst("username"))
          password = form_data.getfirst("password")
        
          if 'login' in form_data:
              result = login.verify(conn, username, password)

          if 'register' in form_data:
              result = login.register(conn, username, password)

          loggedIn = result[0]
          display = result[1]
          userid = result[2]
        
        if loggedIn:
            sess_data['logged_in'] = True
            sess_data['user'] = username
            sess_data['uid'] = userid
            cgi_utils_sda.save_session(my_sess_dir,sessid,sess_data)
            return tmpl.render(top = loggedInTop.format(username = username), choices = loggedInChoices, form = loggedInForm, result = display)
        else:
            cgi_utils_sda.print_headers(None)
            return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)

    if 'logout' in form_data:
        print 'logout'
        sess_data['logged_in'] = False
        cgi_utils_sda.save_session(my_sess_dir,sessid,sess_data)
        return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)

    if 'logged_in' in sess_data and sess_data['logged_in']:
        user = sess_data['user']
    else:
        user = ''

    if user != '':
        display = "Logged in as " + user
        return tmpl.render(top = loggedInTop.format(username = user), choices = loggedInChoices, form = loggedInForm,result = display)
    else:
        return tmpl.render(top = generalTop, choices = generalChoices, form = generalForm, result = display)

if __name__ == '__main__':
    sessid = cgi_utils_sda.session_id()
    print 'Content-type: text/html'
    sess_data = cgi_utils_sda.session_start(my_sess_dir,sessid)
    print

    print '<!-- body follows -->'
    print main()
