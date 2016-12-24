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
import json
# this cgi file looks into each restaurant and see the dishes with their number of like

my_sess_dir = '/students/wzhang2/public_html/cgi-bin/beta/session/'

def main():
    sessid = cgi_utils_sda.session_id()
    sess_data = cgi_utils_sda.session_start(my_sess_dir,sessid)
    print

    # connect to database and set up the env
    conn = search.init()

    env = Environment(loader=FileSystemLoader('./'))
    tmpl = env.get_template('restaurant.html')
    ifLogin = sess_data['logged_in']
    userid = sess_data['uid']
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
        
        if ifLogin:
            link = '''<a href ="res-info-update.cgi?resName={resName}">
            <span id = "mainName">Upload or Update {resName}</span>'''.format(resName=resName)

            # for each dish, if the like is clicked, then it will displayed on the page
            # the like will only be clicked if the user is login, so the for loop will implement only in the login case
            for i in range(len(dishes)):
                if dishes[i]['name'] in form_data:
                    repeat = update.ifRepeatLike(conn,userid,dishes[i]['id'])
                    print repeat
                    if not repeat:
                       dishes[i]['num_of_likes'] += 1 # int
                       # print "yes"
                       # update the database
                       update.incrementLike(conn, dishes[i]['id'], userid, dishes[i]['num_of_likes'])

        else:
            link = '''<a href ="homeLogin.cgi">
            <span id = "mainName">Login to Like and Update</span>'''

        # display the dish info of the restaurant
        dishesDisplay = search.getDishDisplay(dishes, resName,ifLogin)
        return tmpl.render(resName=resName, loca=location, cuisine=cui_type, type=res_type, dishes=dishesDisplay,link = link)

if __name__ == '__main__':
    print 'Content-type: text/html\n'
    print main()
