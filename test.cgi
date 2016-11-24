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
	choices = '''<ul>
	<li><a href="generalS.html"><span id = "mainName">General Search</span>
	  <br><br>Search for an ideal restaurant based on location and type</a>
	<li><a href="dishS.html"><span id = "mainName">Dishes Search</span>
	  <br><br>Search for an ideal restaurant based on your favorite dish</a>
	<li><a href=""><span id = "mainName">Look into Restaurant</span>
	  <br><br>Learn more about specific restaurants</a>
	<li><a href="homepageLogin.html"><span id = "mainName">Login to Contribute</span>
	  <br><br>Login and update the database through adding, liking and commenting</a>
	</ul>'''
	# tmpl = cgi_utils_sda.file_contents('template.html')
	# page = tmpl.format(bottons = choices)
	page = tmpl.render(bottons = choices)
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()
