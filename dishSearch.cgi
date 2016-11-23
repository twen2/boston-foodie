#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader


def main():
	env = Environment(loader=FileSystemLoader('./'))
	tmpl = env.get_template('template.html')
	intro = '''<span id = "mainName">Dish Search</span>
    <br><p><i>Search for an ideal restaurant based on your favorite dish</i>'''

	form = '''<form id= "dishSearch">
	<p>Enter the dish name:
	<input type="text" name="dish">
	<input type="submit" name="submit" value="Search"></form>'''
	
	choices = '''<ul>
	<li><a href="home.cgi"><span id = "mainName">Back to Home Page</span>
	</ul>'''

	page = tmpl.render(intro = intro, searchForm = form, bottons = choices)
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()
