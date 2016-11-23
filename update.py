import sys 
import cgi
import cgitb; cgitb.enable()
# import cgi_utils_sda
import dbconn2
import MySQLdb

def existRes(conn,resName,resLoca):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT * FROM restaurant WHERE name = %s and loca = %s', (resName,resLoca))
	return (curs.rowcount != 0)


