import json
import time
from flask import abort
from flask import Flask, request

app = Flask(__name__)

invite = {'name': 'server',
          'text': 'Welcome to Swisher!',
          'time': time.time()
          }
greeting = {'name': 'bot',
            'text': 'Hey everyone! text /help to ask me something or /train to teach me something',
            'time': time.time()
            }
database = [invite, greeting]
botbase = [{'question': 'hello',
            'answer': 'Hey, dude!'},
           {'question': 'how are you doing',
            'answer': 'I am good.'}]


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
  while True:
    if botbase[j]['question'] == line:
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
              'users': totalusers(database)
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

  msg = {
    'name': name,
    'text': text,
    'time': time.time()
  }
  database.append(msg)

  if text == '/help':
    h = {
      'name': 'bot',
      'text': 'How can I help you?',
      'time': time.time()
    }
    database.append(h)

  if text == '/train':
    tr = {
      'name': 'bot',
      'text': 'Teach me!',
      'time': time.time()
    }
    database.append(tr)

  if database[-3]['text'] == '/help':
    if text[-1] == '?' or text[-1] == '!':
      text = text[:-1]
    answer = {
      'name': 'bot',
      'text': bot(text.lower()),
      'time': time.time()
    }
    database.append(answer)

  if database[-3]['text'] == '/train':
    p = text.find('?')
    if p != -1:
      query = {
        'question': text[:p].lower(),
        'answer': text[p+1:]
      }
      botbase.append(query)
      answer = {
        'name': 'bot',
        'text': 'Thank you, noted.',
        'time': time.time()
      }
    else:
      answer = {
        'name': 'bot',
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
