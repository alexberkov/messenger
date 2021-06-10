import requests
from PyQt6 import QtCore, QtWidgets
import clientui
import datetime

log = ['NULL']


class Messenger(QtWidgets.QMainWindow, clientui.Ui_MainWindow):

  def __init__(self):
    super().__init__()
    self.setupUi(self)

    self.pushButton.pressed.connect(self.send_message)

    self.after = 0
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.get_messages)
    self.timer.start(1000)

  def show_messages(self, messages):
    for message in messages:
      dt = datetime.datetime.fromtimestamp(message['time'])
      self.textBrowser.append(f'{dt.hour}:{dt.minute}:{dt.second}' + ' ' + message['name'])
      self.textBrowser.append(message['text'])
      self.textBrowser.append('')

  def get_messages(self):
    try:
      response = requests.get(
        url='http://127.0.0.1:5000/messages',
        params={'after': self.after}
      )
    except:
      return
    newmessages = response.json()['messages']
    if newmessages:
      self.show_messages(newmessages)
      self.after = newmessages[-1]['time']

  def send_message(self):
    if log[-1] == '/ask':
      receiver = 'bot'
    elif log[-1] == '/train':
      receiver = 'bot-train'
    else:
      receiver = 'everyone'
    name = self.lineEdit.text()
    text = self.textEdit.toPlainText()
    try:
      response = requests.post(
        url='http://127.0.0.1:5000/send',
        json={'name': name, 'text': text, 'receiver': receiver}
      )
      log.append(text)
    except:
      self.textBrowser.append('Server unavailable.')
      self.textBrowser.append('')
      return

    if response.status_code != 200:
      self.textBrowser.append('Incorrect data!')
      self.textBrowser.append('')
      return

    self.textEdit.clear()


app = QtWidgets.QApplication([])
window = Messenger()
window.show()
app.exec()
