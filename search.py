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

    resultSet = getResult(locaSet, resSet, cuiSet)
    return resultSet


def getResult(locaSet, resSet, cuiSet):
    resultSet = []
    for row in locaSet:
        if (row in resSet) and (row in cuiSet):
            resultSet.append(row["name"])

    return resultSet

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

