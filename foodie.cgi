import sys 
import cgi
import cgitb; cgitb.enable()
import cgi_utils_sda
import dbconn2
import MySQLdb



def main():
    dsn = dbconn2.read_cnf(".my.cnf")
    dsn['db'] = 'wzhang2_db'
    dsn['host'] = 'localhost'
    conn = dbconn2.connect(dsn)
    conn.autocommit(True)

    form_data = cgi.FieldStorage()
    tmpl = cgi_utils_sda.file_contents('homepage.html')


if __name__ == '__main__':
    print 'Content-type: text/html\n'
    # displays the webpage
    print main()

    


