import tweepy
from datetime import datetime,date
from secret import consumer_key, consumer_secret, access_token, access_secret, handle

# get authentication info
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# log into the API
api = tweepy.API(auth)
print('[{}] Logged into Twitter API as @{}\n-----------'.format(
    datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
    handle
))

# string array of words that will trigger the on_status function
trigger_words = [
    '@' + handle # respond to @mentions,
]




# override the default listener to add code to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # log the incoming tweet
        # incoming tweet was What is the latest in " "
        holidays={1:[[1,"New year"],[18,"Marlin Luther King Jr"]],
            5: [31,"Memorial"],
            6: [4,"Independence"],
            9: [6,"Labour"],
            11: [[11,"Veterans"],[25,"Thanksgiving"]],
            12: [[24,"Christmas"],[31,"New Year"]]
            }
        print('[{}] Received: "{}" from @{}'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.text,
            status.author.screen_name
        ))

        # get the text from the tweet mentioning the bot.
        # for this bot, we won't need this since it doesn't process the tweet.
        # but if your bot does, then you'll want to use this
        message = status.text
        # respond to the tweet
        dat=str(date.today())
        #dat="2021-11-1"
        time1=365
        event=" b day"
        date_now=dat.split("-")
        if int(date_now[1]) in holidays.keys():
            options=holidays[int(date_now[1])]
            for k in options:
                if int(date_now[2])<k[0]:
                    time1 = k[0]-int(date_now[2])
                    event = k[1]
            if event ==" b day":
                time1=30-int(date_now[2])
                d_now=int(date_now[1])+1
                while d_now not in holidays.keys():
                    time1+=30
                    d_now+=1
                el =holidays[d_now]
                for e in el:
                    if isinstance(e,list):
                        event=e[1]
                        break
                    else:
                        event=e
        else:
            time1=30-int(date_now[2])
            d_now=int(date_now[1])
            next_date=d_now
            while d_now not in holidays.keys():
                time1+=30
                d_now+=1
            el =holidays[d_now]
            for e in el:
                if isinstance(e,list):
                    event=e[1]
                    break
                else:
                    event=e




        response = '@'+ status.author.screen_name + " Next Holiday is about "+ str(time1) +" days away and it is the " + event +" day"
        api.update_status(
            status=response,
            in_reply_to_status_id=status.id
        )
        print('[{}] Responded to @{} with {} day'.format(
            datetime.now().strftime("%H:%M:%S %Y-%m-%d"),
            status.author.screen_name,event
        ))


# create a stream to receive tweets
try:
    streamListener = MyStreamListener()
    stream = tweepy.Stream(auth = api.auth, listener=streamListener)
    stream.filter(track=trigger_words)
except KeyboardInterrupt:
    print('\nGoodbye')
