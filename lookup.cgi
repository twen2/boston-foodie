#!/usr/local/bin/python2.7

import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb
from jinja2 import Environment, FileSystemLoader
import search
import update
# this cgi file looks into each restaurant and see the dishes with their number of like

def main():
    # connect to database and set up the env
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'twen2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)
    env = Environment(loader=FileSystemLoader('./'))
    tmpl = env.get_template('restaurant.html')

    # get the form data
    form_data = cgi.FieldStorage()

    # resID = form_data.getfirst('resID')
    resName = form_data.getfirst('resName')

    if resName == None:
        return tmpl
    else:
        # get the information of the restaurant based on its name
        resInfo = search.getResInfo(conn, resName)
        # general info of the restaurant
        location = resInfo['location']
        cui_type = resInfo['cuisine_type']
        res_type = resInfo['res_type']
        res_id = resInfo['id']
        # search all dishes for this restaurant
        dishes = search.getDishes(conn, res_id)
        # dishList = []
        # for each dish, if the like is clicked, then it will displayed on the page
        # for i in range(len(dishes)):
        #     currDish = ""
        #     # dish = dishes[i]
        #     if dishes[i]['name'] in form_data:
        #         dishes[i]['num_of_likes'] += 1 # int
        #         # update the database
        #         update.incrementLike(conn, dishes[i]['id'], dishes[i]['num_of_likes'])
                # test=dishes[i]['name']
        # display the dish info of the restaurant
        dishesDisplay = search.getDishDisplay(dishes, resName)
        return tmpl.render(resName=resName, loca=location, cuisine=cui_type, type=res_type, dishes=dishesDisplay)

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print main()
