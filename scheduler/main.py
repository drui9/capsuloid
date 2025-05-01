import os
import time
import requests
from threading import Event
from datetime import datetime

remote = os.getenv('WEBAPP_URI', 'http://localhost:8000')
api_key = os.getenv('SECRET_KEY','s3cret1ve')
terminate = Event()

def main():
    head = {
        'api-key': api_key
    }
    while not terminate.is_set():
        timenow = datetime.now().timestamp()
        url = f'{remote}/list'
        resp = requests.get(url, headers=head)
        if resp.ok:
            for item in resp.json().get('scheduled'):
                for ident, tm in item.items():
                    if timenow >= tm:
                        url = f'{remote}/send?id={ident}'
                        requests.get(url, headers=head)
        time.sleep(60*60) # check every hour

if __name__ == '__main__':
    main()

