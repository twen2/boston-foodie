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
    dsn['db'] = 'twen2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)
    tmpl = cgi_utils_sda.file_contents('restaurant-template.html')

    form_data = cgi.FieldStorage()

    resID = form_data.getfirst('resID')
    resInfo = search.getResInfo(conn, resID)
    resName = str(resInfo['resName'])
    location = str(resInfo['loca'])
    cui_type = str(resInfo['cui_type'])
    res_type = str(resInfo['res_type'])
    if resID == None:
        return tmpl
    else:
        return tmpl.format(resName=resName, loca=location, cuisine=cui_type, type=res_type)

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print main()
