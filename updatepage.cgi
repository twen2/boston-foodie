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
	tmpl = env.get_template('updatePage.html')
	page = tmpl.render()
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()
