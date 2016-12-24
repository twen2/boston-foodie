#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader
import search
import update
import json

my_sess_dir = '/students/wzhang2/public_html/cgi-bin/beta/session/'

# this is the cgi for restaurant looking up
def main():
	sessid = cgi_utils_sda.session_id()
	sess_data = cgi_utils_sda.session_start(my_sess_dir,sessid)
	print

	conn = search.init()

	env = Environment(loader=FileSystemLoader('./'))
	tmpl = env.get_template('template.html')

	form_data = cgi.FieldStorage()

	# if restaurant look up form is submitted
	if ("resLookup" in form_data):
		# if dish is entered
		if ("res" in form_data):
			# search if the restaurant name exists
			resResult = search.nameSearch(conn, form_data)
			# display the search result 
			if len(resResult) == 0:
				display = "Sorry, no restaurant with such name exists."
			# if len(resResult) == 1:
			else:
				display = search.displayResult(resResult,"gen")
		else:
			# show the error message to user
			display = "Please enter the restaurant name."
	else:
		display = ""


	# create the restaurant look up page intro
	intro = '''<span id = "mainName">Look Up Restaurant</span>
    <br><p><i>Knowing the restaurant and curious about what it has? Look it up!</i>'''

    # create the restaurant look up form
	form = '''<form id= "lookupRes" method=POST action="lookRes.cgi">
	<p>Enter the restaurant name:
	<input type="text" name="res">
	<input type="submit" name="resLookup" value="Look Up"></form>'''
	
	# create the button to go back to home page
	if sess_data['logged_in']:
		choices = '''<ul><li><a href="homeLogin.cgi"><span id = "mainName">Back to Home Page</span></ul>'''
	else:
		choices = '''<ul><li><a href="home.cgi"><span id = "mainName">Back to Home Page</span></ul>'''

	# render the page in template

	page = tmpl.render(intro = intro, searchForm = form,result = display, bottons = choices)
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()
