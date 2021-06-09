import requests

name = input('Enter name: ')
text = 'NULL'

while True:
  if text == '/ask':
    receiver = 'bot'
    text = input("Ask me: ")
  elif text == '/train':
    receiver = 'bot-train'
    text = input("Enter query: ")
  else:
    receiver = 'everyone'
    text = input()
  response = requests.post(
    url='http://127.0.0.1:5000/send',
    json={'name': name, 'text': text, 'receiver': receiver}
  )
