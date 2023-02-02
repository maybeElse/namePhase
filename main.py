#!python3.10

import datetime
import emoji
import json
import tweepy
import re
import time
import random

import moonphase

def phase_emoji(time: datetime):
    phasename = moonphase.phase(moonphase.position())

    return ":%s_moon:" % phasename.replace(" ", "_").lower()

def get_config() -> dict:
    try:
        config_file = open('config.json', 'r')
        config = json.load(config_file)
    except FileNotFoundError:
        print('config.json does not appear to exist!')
        config = {
            'multiple':false,
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

def get_api(consumer_key, consumer_secret, access_token, access_token_secret) -> tweepy.API:
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
        )

    return tweepy.API(auth)

def update_name(api: tweepy.API):
    user = api.verify_credentials()
    phase = phase_emoji(datetime.datetime.now())

    name = emoji.emojize( 
        (re.sub('\:[a-z_]*_moon\:', '%s',
            emoji.demojize(user.name))
        ) % phase)

    print(name)

    api.update_profile(name=name, skip_status=True)

config = get_config()

if config['multiple'] is True:
    for user in config['tokens']:
        token = config['tokens'][user]
        keys = config['keys']
        api = get_api(
            keys['consumer_key'], keys['consumer_secret'], token['access_token'], token['access_token_secret']
        )
        update_name(api)
        time.sleep(random.random()*3)

else: 
    api = get_api(
        config['tokens']['consumer_key'], config['tokens']['consumer_secret'],
        config['tokens']['access_token'], config['tokens']['access_token_secret'])
    update_name(api)