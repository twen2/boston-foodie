#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader

# this is the file for home page before login
def main():
	env = Environment(loader=FileSystemLoader('./'))
	tmpl = env.get_template('template.html')
	choices = '''<ul>
	<li><a href="genSearch.cgi"><span id = "mainName">General Search</span>
	  <br><br>Search for an ideal restaurant based on location and type</a>
	<li><a href="dishSearch.cgi"><span id = "mainName">Dish Search</span>
	  <br><br>Search for an ideal restaurant based on your favorite dish</a>
	<li><a href="lookRes.cgi"><span id = "mainName">Look into Restaurant</span>
	  <br><br>Learn more about specific restaurants</a>
	<li><a href="homeLogin.cgi"><span id = "mainName">Login to Contribute</span>
	  <br><br>Login and update the database through adding, liking and commenting</a>
	</ul>'''

	page = tmpl.render(bottons = choices)
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()
