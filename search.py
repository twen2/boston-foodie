#!/usr/local/bin/python2.7


import sys 
import cgi
import cgitb; cgitb.enable()
# import cgi_utils_sda
import dbconn2
import MySQLdb

# the file provides helper function for searching

# generally search restaurants by location, cuisine and name
def generalSearch(conn, form_data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)

    loca = form_data.getfirst("location")
    resType = form_data.getfirst("resType")
    cuiType = form_data.getfirst("cuiType")

    curs.execute('SELECT * FROM restaurants')
    # if users don't specify any preference, their choices will be default to the fullset 
    fullSet = curs.fetchall()
    locaSet = fullSet
    resSet = fullSet
    cuiSet = fullSet

    # if users choice any of the selection, the result will be more specific
    if loca != "Unspecified":
        curs.execute('SELECT * FROM restaurants WHERE location = %s', (loca))
        locaSet = curs.fetchall()

    if resType != "Unspecified":
        curs.execute('SELECT * FROM restaurants WHERE res_type = %s', (resType))
        resSet = curs.fetchall()

    if cuiType != "Unspecified":
        curs.execute('SELECT * FROM restaurants WHERE cuisine_type = %s', (cuiType))
        cuiSet = curs.fetchall()

    # return the result set that is the intersection of all three sets
    resultSet = getResult(conn, locaSet, resSet, cuiSet)

    return resultSet

# function that will be helpful when auto-generating the possible location choices for the user
def getLocations(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT DISTINCT(location) FROM restaurants ORDER BY location ASC')
    return curs.fetchall()

# function that will be helpful when auto-generating the possible cuisine type choices for the user
def getCuisines(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT DISTINCT(cuisine_type) FROM restaurants ORDER BY cuisine_type ASC')
    return curs.fetchall()

# return the result set of all satisfied restaurants
def getResult(conn, locaSet, resSet, cuiSet):
    resultSet = []
    for row in locaSet:
        if (row in resSet) and (row in cuiSet):
            resultSet.append(row["name"])

    return resultSet

# return the set of restaurant the has such dishes
def dishSearch(conn, form_data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    dish = cgi.escape(form_data.getfirst("dish"))
    curs.execute('SELECT name FROM restaurants WHERE id in (SELECT res_id FROM dishes WHERE name LIKE %s ORDER BY num_of_likes DESC)', 
        ("%" + dish + "%"))
    dishes = []
    # if the set is not empty, add all restaurants to the list, otherwise return the empty list
    if curs.rowcount != 0:
        resultSet = curs.fetchall()
        for result in resultSet:
            dishes.append(result["name"])
    return dishes

def nameSearch(conn,form_data):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    resname = cgi.escape(form_data.getfirst("res"))
    curs.execute('SELECT name FROM restaurants WHERE name LIKE %s',  ("%" + resname + "%"))
    names = []
    if curs.rowcount != 0:
        resultSet = curs.fetchall()
        for result in resultSet:
            names.append(result["name"])
    return names


# return all information of a restaurant based on its name
# here we suppose no two restaurants have the same name
def getResInfo(conn, resName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM restaurants WHERE name = %s', (resName))
    row = curs.fetchone()
    # result = {}
    # result["resName"] = row['name']
    # result['loca'] = row['location']
    # result['cui_type'] = row['cuisine_type']
    # result['res_type'] = row['res_type']
    # result['id'] = row['id']
    # return result
    return row

# return the id of the restaurant based on the name
# the function will be more useful in the beta version when different restaurants could have the same name
def getResID(conn, resName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM restaurants WHERE name = %s', (resName))
    row = curs.fetchone()
    return row['id']

# the all dishes given the restaurant 
def getDishes(conn, resID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM dishes WHERE res_id = %s ORDER BY num_of_likes DESC', (resID))
    rows = curs.fetchall()
    dishes = []
    # for all dishes, add it to the list by creating a dictionary for each dish
    for row in rows:
        dish = {}
        dish['name'] = row['name']
        dish['num_of_likes'] = row['num_of_likes']
        dish['id'] = row['id']
        dishes.append(dish)
    return dishes

# display the restaurant and dishes nicely with each dish follow up the number of like, and a like button
def getDishDisplay(dishes, resName):
    display = ""
    # if the restaurant has no entered dish, notify users
    if len(dishes) ==0:
        display += "The Restaurant {resName} has no recorded dish now.".format(resName = resName)
    for dish in dishes:
        dishID = dish['id']
        dishName = dish['name']
        dishLikes = dish['num_of_likes']

        display += '''<p id="dish" value={id} like={likes}>{name} &nbsp <span id={id} like={likes}><b>{likes}</b></span> &nbsp 
        <button class="likeB" value={id} like={likes}">like</button></p>'''.format(id=dishID, name=dishName, likes=dishLikes)
        # each like button is a form with unique id
        # display += '''<form id = "dishDisplay" 
        # method = POST 
         # onclick="incrementLike({id},{likes})
        # action = "lookup.cgi?resName={resName}"><p value = "{id}">{name} &nbsp <span><b>{likes}</b></span>  &nbsp 
        # <input type="submit" id = "like{id}" name = "{name}" value = "LIKE"></p></form>'''.format(id=dishID, name=dishName, likes=dishLikes, resName=resName)

    return display

# display each restaurant result with a hyperline
# when calling this function, we suppose the result set is not empty
# The empty case has been handle before the function is called
# def displayResult(resultSet):
#         display = "<h3>Matching Restaurants</h3>"
#         for re in resultSet:
#             display += '''<p><a href="lookup.cgi?resName={resName}">{resName}</a>'''.format(resName=re)
#         return display
    

def displayResult(resultSet,info):
    if info == "gen":
        display = "<h3>Matching Restaurants</h3>"
        for re in resultSet:
            display += '''<p><a href="lookup.cgi?resName={resName}">{resName}</a>'''.format(resName=re)
        return display
    else: 
        # if the info is a dish name
        display = "<h3>Restaurants that have {dish} ranked by # of likes</h3>".format(dish = info)
        for re in resultSet:
            display += '''<p><a href="lookup.cgi?resName={resName}">{resName}</a>
            <span>{number} likes</span>'''.format(resName=re,number=0)
        return display






