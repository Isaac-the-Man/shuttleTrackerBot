import os
from dotenv import load_dotenv
import sys
import requests
from discord_webhook import DiscordWebhook
from time import sleep


# load env var
load_dotenv()
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
PING_URL = os.getenv('PING_URL')
INTERVAL = int(os.getenv('SCRAPE_INTERVAL'))
MAX_FAIL = int(os.getenv('MAX_FAIL'))
for var in [WEBHOOK_URL, PING_URL, INTERVAL, MAX_FAIL]:
    if var is None:
        # missing .env vars
        print('Missing one or more .env variables, terminating...')
        sys.exit(1)
print('Starting ShuttleTrackerBot...')
webhook = DiscordWebhook(url=WEBHOOK_URL, content='ShuttleTrackerBot is now online !!!')
response = webhook.execute()

# ping server
now = 0
cum_failures = 0
is_online = True # True for online, False otherwise
while(True):
    sleep(1)
    # check interval
    if now >= INTERVAL:
        print(f'Attempting to ping {PING_URL}...')
        # reset time
        now = 0
        # ping server
        isPingSuccess = True
        try:
            r = requests.get(PING_URL)
            if r.status_code != 200:
                # bad status code
                isPingSuccess = False
                print(f'FAILED: status {r.status_code}')
        except requests.exceptions.RequestException as e:
            # Timeout, TooManyRedirects, ConnectionError, or HTTPError
            print(f'FAILED: {type(e).__name__}')
            isPingSuccess = False
        if is_online and not isPingSuccess:
            # unsuccessful ping
            cum_failures += 1
            # check if maximum failure tolerance is met
            if cum_failures >= MAX_FAIL:
                # flip status
                is_online = False
                # alert discord
                webhook = DiscordWebhook(url=WEBHOOK_URL, content='Server offline :eyes:')
                response = webhook.execute()
            continue
        elif not is_online and isPingSuccess:
            print('SUCCESS')
            # server recovered
            is_online = True
            cum_failures = 0
            # alert discord
            webhook = DiscordWebhook(url=WEBHOOK_URL, content='Server recovered !!!')
            response = webhook.execute()
            continue
        if isPingSuccess:
            # successful ping
            print('SUCCESS')

    # increment time
    now += 1