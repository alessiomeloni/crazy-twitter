import tweepy
import json
from time import sleep
from random import shuffle
import random
import time
import datetime
import pytz
import logging
import platform
import os

######## Logging Config ########
FORMAT = ('[%(asctime)s] - %(levelname)s : %(message)s')
logging.basicConfig(format=FORMAT, level=logging.INFO)
######## Logging Config ########

# function to check if there's a network connection
def checkList():
    system_os=platform.system()
    while True:
        hostname = "1.1.1.1"
        if system_os == "Linux":
            cmd = "ping -c 1 "
        if system_os == "Windows":
            cmd = "ping -n 1 "

        response = os.system(cmd + hostname)

        if response == 0:
          logging.info("NETWORK:\t[ONLINE]")
          break
        else:
          logging.warning("NETWORK:\t[OFFLINE]")
          time.sleep(1)

# function to get list of followers and followings, gets whitelisted users
def get_friends():
    # gets a list of your followers and following
    followers = api.followers_ids(screen_name)
    following = api.friends_ids(screen_name)
    total_followed = 0

    whitelisted_users = []

    # convert screen names to user IDs
    for item in config_data["whitelisted_accounts"]:
        try:
            # gets info, then gets id.
            item = api.get_user(screen_name=item).id
            # adds the id into newlist.
            whitelisted_users.append(item)
        except tweepy.TweepError:
            pass

    # blacklist users to not folllow - declaring a variable name to minimize confusion.
    blacklisted_users = config_data["blacklisted"]

    return followers, following, total_followed, whitelisted_users, blacklisted_users

# function to follow the followers of another user.
def follow_all(followers, following, total_followed, whitelisted_users, blacklisted_users, target):
    their_name = target
    their_followers = api.followers_ids(their_name)

    # Makes a list of nonmutual followings.
    their_followers_reduced = set(their_followers) - set(following) - set(blacklisted_users)
    # loops through their_followers and followers and adds non-mutual relationships to their_followers_reduced

    logging.info('Starting to follow users...')
    # loops through the list and follows users.
    for f in their_followers_reduced:
        try:
            # follows the user.
            api.create_friendship(f)
            total_followed += 1
            if total_followed % 10 == 0:
                logging.info(str(total_followed) + ' users followed so far.')
            delay =  random.randint(2*60, 20*60)
            logging.info(f'Followed user. Sleeping {delay} seconds.')
            sleep(delay)
        except (tweepy.RateLimitError, tweepy.TweepError) as e:
            error_handling(e)
    logging.info(total_followed)

# function to unfollow all users.
def unfollow_all(followers, following, total_followed, whitelisted_users, blacklisted_users):
    # whitelists some users.
    unfollowing_users = set(following) - set(whitelisted_users)
    logging.info('Starting to unfollow.')
    for f in unfollowing_users:
        # unfollows user
        api.destroy_friendship(f)
        # increment total_followed by 1
        total_followed += 1
        # logging.info total unfollowed every 10
        if total_followed % 10 == 0:
            logging.info(str(total_followed) + ' unfollowed so far.')
        # logging.info sleeping, sleep.
        delay =  random.randint(2*60, 20*60)
        logging.info(f'Followed user. Sleeping {delay} seconds.')
        sleep(delay)
    logging.info(total_followed)

# function to unfollow users that don't follow you back.
def unfollow_back(followers, following, total_followed, whitelisted_users, blacklisted_users):
    logging.info('Starting to unfollow users...')
    # makes a new list of users who don't follow you back.
    non_mutuals = set(following) - set(followers) - set(whitelisted_users)
    for f in non_mutuals:
        try:
            # unfollows non follower.
            api.destroy_friendship(f)
            total_followed += 1
            if total_followed % 10 == 0:
                logging.info(str(total_followed) + ' unfollowed so far.')

            delay =  random.randint(2*60, 20*60)
            logging.info(f'Unofollowed user. Sleeping {delay} seconds.')
            sleep(delay)
        except (tweepy.RateLimitError, tweepy.TweepError) as e:
            error_handling(e)
    logging.info(total_followed)

# function to handle errors
def error_handling(e):
    error = type(e)
    sleeping_time = random.randint(30*60, 60*60)

    if error == tweepy.RateLimitError:
        logging.error(f"You've hit a limit! Sleeping for {sleeping_time} minutes.")
        sleep(sleeping_time)
    if error == tweepy.TweepError:
        logging.warning(f'Uh oh. Could not complete task. Sleeping {sleeping_time} seconds.')
        sleep(sleeping_time)

def main():
    while True:
        now = pytz.timezone(time_zone).localize(datetime.datetime.now())

        timing_admin_start_time = now.replace(hour=start_time_hour, minute=start_time_minute, second=0, microsecond=0)
        timing_admin_end_time = now.replace(hour=end_time_hour, minute=end_time_minute, second=0, microsecond=0)
        while now > timing_admin_start_time and now < timing_admin_end_time or debug:
            target = random.choice(targets)
            logging.info(f"TARGET:\t{target}")
            follow_all(*get_friends(), target=target)
            unfollow_back(*get_friends())
        time.sleep(10)

if __name__ == "__main__":
    checkList()
    # gets all of our data from the config file.
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        logging.info("Getting the configuration file")
    screen_name = config_data["auth"]["screen_name"]

    # authorization from values inputted earlier, do not change.
    auth = tweepy.OAuthHandler(config_data["auth"]["CONSUMER_KEY"], config_data["auth"]["CONSUMER_SECRET"])
    auth.set_access_token(config_data["auth"]["ACCESS_TOKEN"], config_data["auth"]["ACCESS_SECRET"])
    api = tweepy.API(auth)

    # debug
    debug = config_data["debug"]

    # Working Time
    time_zone = config_data["time_zone"]
    start_time = config_data["start_time"]
    end_time = config_data["end_time"]
    # Hours
    start_time_hour=int(start_time.split(":")[0])
    end_time_hour=int(end_time.split(":")[0])
    # Minutes
    start_time_minute=int(start_time.split(":")[1])
    end_time_minute=int(end_time.split(":")[1])

    targets = config_data["targets"]

    # Starting the main thread
    main()
