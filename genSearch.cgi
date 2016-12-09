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
	if ("generalS" in form_data):
		results = search.generalSearch(conn, form_data)
		display = search.displayResult(results)

	env = Environment(loader=FileSystemLoader('./'))
	tmpl = env.get_template('template.html')

	locaRows = search.getLocations(conn)
	locaOptions = ''''''
	for row in locaRows:
		locaOptions+='''<option value = "{row[location]}">{row[location]}</option>'''.format(row=row)

	cuisineRows = search.getCuisines(conn)
	cuisineOptions = ''''''
	for row in cuisineRows:
		cuisineOptions+='''<option value = "{row[cuisine_type]}">{row[cuisine_type]}</option>'''.format(row=row)


	intro = '''<span id = "mainName">General Search</span>
	<br><p><i>Search for an ideal restaurant based on location and type</i>'''

	form = '''<form id = "generalSearch" method = POST action = "genSearch.cgi" style = "text-indent: 10px">
	<p>Please select a location:
	<select name="location">
	   <option value="Unspecified">Unspecified</option>
	   {locaOptions}
	</select></p>
	<p>Please select the restaurant type:
	<select name="resType">
	<option value="Unspecified">Unspecified</option>
	<option value="meal">meal</option>
	<option value="cafe">cafe</option>
	</select></p>
	<p>Please select the cuisine type:
	<select name="cuiType">
	<option value="Unspecified">Unspecified</option>
	   {cuisineOptions}
	</select></p>
	<p><input type="submit" name="generalS" value="Search"></form>
	'''.format(locaOptions=locaOptions,cuisineOptions=cuisineOptions)

	choices = '''<ul>
	<li><a href="home.cgi"><span id = "mainName">Back to Home Page</span>
	</ul>'''

	page = tmpl.render(intro = intro, searchForm = form, result = display, bottons = choices)
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()