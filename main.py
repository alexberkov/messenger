import datetime
import time

message1 = {'name': 'Jack',
            'text': 'Hello everyone!',
            'time': time.time()
            }
message2 = {'name': 'Mary',
            'text': 'Hello, Jack!',
            'time': time.time()
            }
database = [message1, message2]


def send_message(name, text):
    tmp = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    database.append(tmp)


send_message('Admin', 'You are banned!')
send_message('Jack', 'Please no!')


def print_messages(messages):
    for message in messages:
        dt = datetime.datetime.fromtimestamp(message['time'])
        print(f'{dt.hour}:{dt.minute}:{dt.second}', message['name'])
        print(message['text'])
        print()


def get_messages(after):
    messages = []
    for element in database:
        if element['time'] > after:
            messages.append(element)

    return messages


messagesFull = get_messages(0)
last = messagesFull[-1]['time']
send_message('Alex', 'I am new here...')
send_message('Joyce', 'Yeah, me too :)')
messagesFull = get_messages(last)
print_messages(messagesFull)
