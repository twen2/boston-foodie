#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader


def main():
	dsn = dbconn2.read_cnf(".my.cnf")
	dsn['db'] = 'wzhang2_db'
	dsn['host'] = 'localhost'
	conn = dbconn2.connect(dsn)
	conn.autocommit(True)

	env = Environment(loader=FileSystemLoader('./'))
	tmpl = env.get_template('resEdit.html')

	form_data = cgi.FieldStorage()
	resname = form_data.getfirst('resName')

	# if resName = None:
	# 	return tmpl
	# else:
	page = tmpl.render(resName = "None", default_loca = "None", default_cuisine = "None",message = "")
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()