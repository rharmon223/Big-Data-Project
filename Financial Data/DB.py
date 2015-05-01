import psycopg2
import sqlite3

DB_NAME = 'Big Data'

'''
I am running the codes in my local computer. You need to change the self.conn to make it run.
'''
class DB:
        def __init__(self, db_name):
		try:
			self.conn = psycopg2.connect("dbname='%s' user='postgres' host='localhost' password='140512'" % db_name)
		except:
			print "I am unable to connect to the database"
			exit()
                self.cur = self.conn.cursor()

        def cursor(self):
                return self.cur
        def getNewCursor(self):
                return self.conn.cursor()
        def connection(self):
                return self.conn

	def query(self, q):
		self.cur.execute(q)
		return self.cur.fetchall()