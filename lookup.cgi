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
    env = Environment(loader=FileSystemLoader('./'))
    tmpl = env.get_template('restaurant.html')

    form_data = cgi.FieldStorage()

    # resID = form_data.getfirst('resID')
    resName = form_data.getfirst('resName')

    if resName == None:
        return tmpl
    else:
        resInfo = search.getResInfo(conn, resName)
        # resName = str(resInfo['resName'])
        # location = str(resInfo['loca'])
        # cui_type = str(resInfo['cui_type'])
        # res_type = str(resInfo['res_type'])
        location = resInfo['location']
        cui_type = resInfo['cuisine_type']
        res_type = resInfo['res_type']
        res_id = resInfo['id']
        dishes = search.getDishes(conn, res_id)
        dishesDisplay = search.getDishDisplay(dishes)
        return tmpl.render(resName=resName, loca=location, cuisine=cui_type, type=res_type, dishes=dishesDisplay)

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print main()
