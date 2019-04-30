import twitter
import json
import sqlite3
import pytumblr
import os
import time


### EDIT CONTENT ###
# Accounts to get tweets from
accounts = [ '' ] # Twitter accounts to use
names = [ '' ] # Will be used for tags
images = [ '' ] # Links to any images you wish to use
blog_name = '' # Tumblr blog to use
db_file = 'connect.db'
sleep_time = 21600 # Sleep for 6 hours before getting more tweets

# Twitter Keys - Sensitive Info
# Fill in with your own keys
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='',
                  tweet_mode='extended')

# Fill in with your own keys
client = pytumblr.TumblrRestClient(
  '',
  '',
  '',
  ''
)

##################

client.info()

def Check_Twitter_Connection():
    if api.VerifyCredentials() is not None:
        verified=True

    print(verified)

def Get_Tweets():
    for a in accounts:
        t = api.GetUserTimeline(screen_name=a, count=2)

        tweets = [i.AsDict() for i in t]

        for t in tweets:
            Append_Data(a, t)

def Append_Data(a, t):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO tweets VALUES (?, ?, ?)', (t['id'], a, t['full_text']))
        Tumblr_Post(a, t)
    except Exception as e:
        print("Exception message: " + str(e))
        print("Tweet info: " + str(t['id']) + " - " + a)
    finally:
        conn.commit()
        
def Initialize_Database():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tweets (
                 id integer PRIMARY KEY,
                 name text NOT NULL,
                 t text NOT NULL
             )''')
    conn.commit()
    conn.close()

def Check_Data():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('SELECT * from tweets')
    print(c.fetchall())
    conn.close()

def Tumblr_Post(a, t):
    #print(json.dumps(t, indent=4, sort_keys=True))
    text = '<h2><b>' + t['full_text'] + '</b></h2>' + "<a href=\"https://twitter.com/" + a + "/status/" + str(t['id']) + "\">From Twitter</a>"
    print(text)
    client.create_photo(blog_name, state="queue", tags=[names[accounts.index(a)]], caption=text, source=images[accounts.index(a)])

Check_Twitter_Connection()
Initialize_Database()
while True:
    Get_Tweets()
    Check_Data()
    time.sleep(sleep_time) 
