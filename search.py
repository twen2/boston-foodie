#!/usr/local/bin/python2.7


import sys 
import cgi
import cgitb; cgitb.enable()
# import cgi_utils_sda
import dbconn2
import MySQLdb

def generalSearch(conn, form_data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    loca = form_data.getfirst("location")
    resType = form_data.getfirst("resType")
    cuiType = form_data.getfirst("cuiType")

    curs.execute('SELECT * FROM restaurants')
    fullSet = curs.fetchall()
    locaSet = fullSet
    resSet = fullSet
    cuiSet = fullSet

    if loca != "Unspecified":
        curs.execute('SELECT * FROM restaurants WHERE location = %s', (loca))
        locaSet = curs.fetchall()

    if resType != "Unspecified":
        curs.execute('SELECT * FROM restaurants WHERE res_type = %s', (resType))
        resSet = curs.fetchall()

    if cuiType != "Unspecified":
        curs.execute('SELECT * FROM restaurants WHERE cuisine_type = %s', (cuiType))
        cuiSet = curs.fetchall()

    resultSet = getResult(conn, locaSet, resSet, cuiSet)

    return resultSet


def getResult(conn, locaSet, resSet, cuiSet):
    resultSet = []
    for row in locaSet:
        if (row in resSet) and (row in cuiSet):
            resultSet.append(str(row["name"]))

    display = "<h3>Matching Restaurants</h3>"
    for re in resultSet:
        # display += '''<p><a href = "">{re}</a>'''.format(re=re)
        resID = getResID(conn, re)
        display += '''<a href="searchResult.cgi?resID={resID}">{resName}</a>'''.format(resID, re)

    return display

def dishSearch(conn, form_data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    dish = form_data.getfirst("dish")
    curs.execute('SELECT * FROM dishes WHERE name LIKE %s', ("%" + dish + "%"))
    if curs.rowcount == 0:
        return "Sorry, no dishes match your search."
    else:
        resultSet = curs.fetchall()
        dishes = []
        for result in resultSet:
            dishes.append(result["name"])
        return dishes

def getResInfo(conn, resID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM restaurants WHERE id = %s', (resID))
    row = curs.fetchone()
    result = {}
    result["resName"] = row['name']
    result['loca'] = row['location']
    result['cui_type'] = row['cuisine_type']
    result['res_type'] = row['res_type']
    # result['id'] = row['id']
    return result

def getResID(conn, resName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM restaurants WHERE name = %s', (resName))
    row = curs.fetchone()
    return row['id']

def getDishes(conn, resID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM dishes WHERE res_id = %s', (resID))
    rows = curs.fetchall()
    dishes = []
    for row in rows:
        dish = {}
        dish['name'] = row['name']
        dish['num_of_likes'] = row['num_of_likes']
        dish['id'] = row['id']
        dishes.append(dish)
    return dishes