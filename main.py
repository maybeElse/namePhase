#!python3.10

import datetime
import emoji
from astral import moon
import json
import tweepy
import re

def phase_emoji(time: datetime):
    phase = moon.phase(time)

    if phase < 3: # new moon
        return (phase, ":new_moon:")
    elif phase < 6.5: # waxing crescent
        return (phase, ":waxing_crescent_moon:")
    elif phase < 9: # first quarter
        return (phase, ":first_quarter_moon:")
    elif phase < 12: # waxing gibbous
        return (phase, ":waxing_gibbous_moon:")
    elif phase < 17.5: # full moon
        return (phase, ":full_moon:")
    elif phase < 20: # waning gibbous
        return (phase, ":waning_gibbous_moon:")
    elif phase < 23: # last quarter
        return (phase, ":last_quarter_moon:")
    elif phase < 27: # waning crescent
        return (phase, ":waning_crescent_moon:")
    else:
        return (phase, ":new_moon:")

def get_config() -> dict:
    try:
        config_file = open('config.json', 'r')
        config = json.load(config_file)
    except FileNotFoundError:
        print('config.json does not appear to exist!')
        config = {
            'tokens':{
                'consumer_key':'', 'consumer_secret':'', 'access_token':'', 'access_token_secret':''
                }
            } 
        with open('config.json', 'w') as outfile:
            json.dump(config, outfile, indent=4)
            print("I've created it, please fill it out :)")
            outfile.close
            quit()
    except json.JSONDecodeError as err:
        print('JSONDecodeError: {0}'.format(err))
        quit
    else:
        return config

def get_api() -> tweepy.API:
    config=get_config()

    auth = tweepy.OAuth1UserHandler(
        config['tokens']['consumer_key'], config['tokens']['consumer_secret'],
        config['tokens']['access_token'], config['tokens']['access_token_secret']
        )

    return tweepy.API(auth)
                  
api = get_api()
user = api.verify_credentials()
phase = phase_emoji(datetime.datetime.now())

# name = emoji.demojize(user.name) # change emoji to :emoji_name: format
# name = (re.sub('\:[a-z_]*_moon\:', '%s', name)) # replace moon emoji with %s
# name = emoji.emojize(name % phase[1]) # insert new emoji into name

name = emoji.emojize( 
    (re.sub('\:[a-z_]*_moon\:', '%s',
        emoji.demojize(user.name))
    ) % phase[1])

# print(name)

api.update_profile(name=name, skip_status=True)