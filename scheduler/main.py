import os
import time
import requests
from loguru import logger
from threading import Event
from datetime import datetime

remote = os.getenv('WEBAPP_URI', 'http://localhost:8000')
api_key = os.getenv('SECRET_KEY','s3cret1ve')
sleeptime = 60 * 60 # check every hour
terminate = Event()

# --
def main():
    head = {
        'api-key': api_key
    }
    while not terminate.is_set():
        timenow = datetime.now().timestamp()
        url = f'{remote}/list'
        try:
            resp = requests.get(url, headers=head)
            if resp.ok:
                for item in resp.json().get('scheduled'):
                    for ident, tm in item.items():
                        if timenow >= tm:
                            url = f'{remote}/send?id={ident}'
                            logger.debug('Sending: {}', url)
                            requests.get(url, headers=head)
            time.sleep(sleeptime)
        except Exception:
            logger.exception('what?')
            time.sleep(10)

if __name__ == '__main__':
    main()

