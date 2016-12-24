#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader
import search
import json

my_sess_dir = '/students/wzhang2/public_html/cgi-bin/beta/session/'

# this is the cgi for dish search
def main():
	sessid = cgi_utils_sda.session_id()
	sess_data = cgi_utils_sda.session_start(my_sess_dir,sessid)
	print

	conn = search.init()

	form_data = cgi.FieldStorage()

	# if dish search form is submitted
	if ("dishS" in form_data):
		# if dish is entered
		if ("dish" in form_data):
			# search all restaurant with dishes similar to the dish name entered
			allResults = search.dishSearch(conn, form_data)
			dishname = cgi.escape(form_data.getfirst("dish"))
			# display the search result 
			if len(allResults) == 0:
				display = "Sorry, no restaurant has such dish"
			else:
				display = search.displayResult(allResults,dishname)
		else:
			# show the error message to user
			display = "Please enter the dish name."
	else:
		display = ""

	env = Environment(loader=FileSystemLoader('./'))
	tmpl = env.get_template('template.html')

	# create the dish search page intro
	intro = '''<span id = "mainName">Dish Search</span>
    <br><p><i>Search for an ideal restaurant based on your favorite dish</i>'''

    # create the dish search form
	form = '''<form id= "dishSearch" method=POST action="dishSearch.cgi">
	<p>Enter the dish name:
	<input type="text" name="dish">
	<input type="submit" name="dishS" value="Search"></form>'''
	
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
