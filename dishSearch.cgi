#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader
import search


def main():
	dsn = dbconn2.read_cnf(".my.cnf")
	dsn['db'] = 'wzhang2_db'
	dsn['host'] = 'localhost'
	conn = dbconn2.connect(dsn)
	conn.autocommit(True)

	form_data = cgi.FieldStorage()
	display = ""
	if "dishS" in form_data:
		if "dish" in form_data:
			display = search.dishS(conn, form_data)
		else:
			display += "Please enter the dish name."

	env = Environment(loader=FileSystemLoader('./'))
	tmpl = env.get_template('template.html')
	intro = '''<span id = "mainName">Dish Search</span>
    <br><p><i>Search for an ideal restaurant based on your favorite dish</i>'''

	form = '''<form id= "dishSearch" method=POST action="dishSearch.cgi">
	<p>Enter the dish name:
	<input type="text" name="dish">
	<input type="submit" name="dishS" value="dishS"></form>'''
	
	choices = '''<ul>
	<li><a href="home.cgi"><span id = "mainName">Back to Home Page</span>
	</ul>'''

	page = tmpl.render(intro = intro, searchForm = form,result = display, bottons = choices)
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()
