import json
import time
import re
from flask import abort
from flask import Flask, request

app = Flask(__name__)

invite = {'name': 'Server',
          'text': 'Welcome to Swisher!',
          'time': time.time()
          }
greeting = {'name': 'Swish-bot',
            'text': 'Hey everyone! text /help for help :)',
            'time': time.time()
            }

bothelp = 'Commands: /ask to ask me! '
bothelp += '/train to train me! '
bothelp += '/count to get the number of messages! '
bothelp += '/users to get the number of users!'

database = [invite, greeting]
botbase = [{'question': 'hello',
            'answer': 'Hey, dude!'},
           {'question': 'how are you doing',
            'answer': 'I am good.'},
           {'question': 'why swisher',
            'answer': 'Cause every message is nothing but net!'}]


def totalusers(base: list):
  users = []
  i = 0
  while True:
    curr = base[i]['name']
    if curr not in users:
      users.append(curr)
    if i == len(base) - 1:
      break
    i += 1
  return len(users)


def bot(line: str):
  j = 0
  question = re.compile(line)
  while True:
    query = re.compile(botbase[j]['question'])
    if question.search(botbase[j]['question']) or query.search(line):
      return botbase[j]['answer']
    if j == len(botbase) - 1:
      break
    j += 1
  return 'Sorry, I am unable to help you.'


@app.route("/")
def hello():
  return "<h2> Hello, Skillbox </h2> <br> <a href='/status'> Status </a> <br> <a href='/about_us'> About Us </a>"


@app.route("/status")
def status():
  response = {'status': 'true',
              'name': 'Swisher',
              'messages': len(database),
              'users': totalusers(database),
              'time': time.asctime()
              }
  return json.dumps(response)


@app.route("/about_us")
def about_us():
  description: str = "<h2> Welcome! </h2> <p> We are a new Flask-based messenger called Swisher! </p>"
  return description


@app.route("/send", methods=['POST'])
def send_message():
  data = request.json

  if not isinstance(data, dict):
    return abort(400)
  if 'name' not in data or 'text' not in data:
    return abort(400)

  name = data['name']
  text = data['text']

  if not isinstance(name, str) or not isinstance(text, str):
    return abort(400)
  if not 0 < len(name) <= 128:
    return abort(400)
  if not 0 < len(name) <= 1000:
    return abort(400)

  if 'receiver' in data and isinstance(data['receiver'], str):
    receiver = data['receiver']
  else:
    receiver = 'everyone'

  msg = {
    'name': name,
    'text': text,
    'time': time.time()
  }
  database.append(msg)

  if text == '/help':
    h = {
      'name': 'Swish-bot',
      'text': bothelp,
      'time': time.time()
    }
    database.append(h)

  if text == '/ask':
    a = {
      'name': 'Swish-bot',
      'text': 'Ask me: ',
      'time': time.time()
    }
    database.append(a)

  if text == '/train':
    t = {
      'name': 'Swish-bot',
      'text': 'Train me: ',
      'time': time.time()
    }
    database.append(t)

  if text == '/count':
    c = {
      'name': 'Swish-bot',
      'text': 'Total messages: ' + str(len(database)),
      'time': time.time()
    }
    database.append(c)

  if text == '/users':
    u = {
      'name': 'Swish-bot',
      'text': 'Total users: ' + str(totalusers(database)),
      'time': time.time()
    }
    database.append(u)

  if receiver == 'bot':
    if text[-1] == '?' or text[-1] == '!':
      text = text[:-1]
    answer = {
      'name': 'Swish-bot',
      'text': bot(text.lower()),
      'time': time.time()
    }
    database.append(answer)

  if receiver == 'bot-train':
    p = text.find('?')
    if p != -1:
      query = {
        'question': text[:p].lower(),
        'answer': text[p+1:]
      }
      botbase.append(query)
      answer = {
        'name': 'Swish-bot',
        'text': 'Thank you, noted.',
        'time': time.time()
      }
    else:
      answer = {
        'name': 'Swish-bot',
        'text': 'Incorrect request!',
        'time': time.time()
      }
    database.append(answer)

  return {'ok': True}


@app.route("/messages")
def get_messages():
  try:
    after = float(request.args['after'])
  except:
    return abort(400)

  messages = []
  for element in database:
    if element['time'] > after:
      messages.append(element)

  return {'messages': messages[:50]}


app.run()
