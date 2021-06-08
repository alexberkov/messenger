import time

import requests
import datetime


def print_messages(messages):
  for message in messages:
    dt = datetime.datetime.fromtimestamp(message['time'])
    print(f'{dt.hour}:{dt.minute}:{dt.second}', message['name'])
    print(message['text'])
    print()


after = 0

while True:
  response = requests.get(
    url='http://127.0.0.1:5000/messages',
    params={'after': after}
  )
  newmessages = response.json()['messages']
  if newmessages:
    print_messages(newmessages)
    after = newmessages[-1]['time']
  time.sleep(1)
