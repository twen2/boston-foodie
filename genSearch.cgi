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
	intro = '''<span id = "mainName">General Search</span>
	<br><p><i>Search for an ideal restaurant based on location and type</i>'''

	form = '''<form id = "generalSearch" style = "text-indent: 10px">
	<p>Please select a location:
	<select name="location">
	<option value="Unspecified">Unspecified</option>
	<option value="Boston">Boston</option>
	<option value="Cambridge">Cambridge</option>
	<option value="Wellesley">Wellesley</option>
	<option value="Newton">Newton</option>
	<option value="Natick">Natick</option>
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
	<option value="Japanese">Japanese</option>
	<option value="Thai">Thai</option>
	<option value="Chinese">Chinese</option>
	<option value="Italian">Italian</option>
	<option value="French">French</option>
	<option value="American">American</option>
	<option value="Korean">Korean</option>
	</select></p>

	<p><input type="submit" name="submit" value="Search"></form>'''

	choices = '''<ul>
	<li><a href="home.cgi"><span id = "mainName">Back to Home Page</span>
	</ul>'''

	page = tmpl.render(intro = intro, searchForm = form, bottons = choices)
	return page

if __name__ == '__main__':
	print 'Content-type: text/html\n'
	print main()