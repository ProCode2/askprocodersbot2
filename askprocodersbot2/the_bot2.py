import tweepy
import psycopg2
import time
import os


print("this bot is working")
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY , CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY , ACCESS_SECRET)
api = tweepy.API(auth)

def connect_to_database():
	global c
	global con
	DATABASE_URL = os.environ['DATABASE_URL']
	con = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = con.cursor()
	print('connected to database')


def upload_answer():
	c.execute('''SELECT name,id,answers,send FROM qa WHERE answers IS NOT NULL AND send IS NULL ''')
	rows = c.fetchall()
	print(rows)
	for r in rows:
		print(r)
		api.update_status('@' + r[0] + ''' - ''' + r[2], r[1])
		c.execute(''' UPDATE qa SET send ='sent' WHERE id = (%s)''', [r[1]])
		con.commit()
		print(r[0])



def disconnect():
	c.close()
	con.close()
	print('disconnected')

connect_to_database()

while True:
	upload_answer()
	time.sleep(2)

disconnect()
