from pathlib import Path
from alarm.alarm import Alarm
from alarm.alarm_types import alarm_types
from tools.tools import Tools

# Menu
# startar alarm skapande dialog
# options - add alarm, remove alarm, start monitor
# m = Monitor(Alarm(type, target), Alarm(type, target), Alarm(type, target))
# m.start(), m.stop()
# Startar monitor -> m.start()
# avslutar monitors arbete (ctrl c) -> m.stop()
# try:
#   m.start()
# except KeyboardInteruption:
#   m.stop() 
# handlar errors ?
menu_messages = {
  'menu': {
    'start': 'Welcome to our smal monitoring system',
    'no_alarms': 'To start to work with the monitoring you need to create alarms'
  },
  'alarm': {
    'start_create': 'what type of alarm would you like to create',
    'existed': 'Alarm, {type} exists. Do you want to replace it?'
  }
}

class Menu(Tools):
  alarms_file = Path.cwd() / 'alarms' / 'alarms.txt'
  alarms = []
  yesNoOptions = {
    '0': {
      'text': 'No',
    },
    '1': {
      'text': 'Yes',
    },
  }

  def __init__(self):
    self.checkAlarmsFile()
    self.parseAlarms()
    self.options = {
        '0': {
          'text': 'Create new alarm',
          'fn': self.createAlarms
        },
        '1': {
          'text': 'Change existing alarm'
        },
        '2': {
          'text': 'Start monitoring'
        }
      }

  def checkAlarmsFile(self):
    if not self.alarms_file.exists():
      self.alarms_file.touch()

  def parseAlarms(self):
    with self.alarms_file.open('r') as file:
      data = file.readlines()
      if len(data):
        self.alarms = [Alarm(line.strip()) for line in data]

  def start(self):
    print(menu_messages['menu']['start'])
    self.printAlarms()

    while True:
      if not len(self.alarms):
        print(menu_messages['menu']['no_alarms'])
        self.createAlarms()
      else:
        self.showOptions()

  def showOptions(self):
    print('Existing alarms')
    self.printAlarms()
    print('What is next?')

    choice = self.requestAnswer(self.options)
    chosenOption = self.options[str(choice)]

    if 'fn' in chosenOption and callable(chosenOption.get('fn')): 
      chosenOption['fn']()
    else: print('not ready yet')

  def requestAnswer(self, options):
    self.printOptions(options)
    maxIndex = self.getMaxIndex(options)
    return self.requestNumberBetween(maxIndex)

  def printOptions(self, options):
    for i, option in options.items():
      print(f'{i} - {option['text']}')

  def getMaxIndex(self, collection):
    return max(
      [int(i) for i in collection.keys()]
    )

  def printAlarms(self):
    if not len(self.alarms):
      return print('There is no alarms in the system')
    print('\nThe list of alarms')
    for alarm in self.alarms:
      print(alarm)

  def createAlarms(self):
    print(menu_messages['alarm']['start_create'])
    self.printAvailableAlarmTypes()
    type = alarm_types[
      self.requestNumberBetween(len(alarm_types) - 1)
    ]

    print('Set alarm value')
    target = self.requestNumberBetween(100)

    if self.isAlarmExist(type):
      print(menu_messages['alarm']['existed'].format(type=type))
      choice = self.requestAnswer(self.yesNoOptions)
      if choice:
        self.replaceAlarm(Alarm(type, target))
    else:
      self.alarms.append(Alarm(type, target))

  def replaceAlarm(self, newAlarm):
    for i, alarm in enumerate(self.alarms):
      if alarm.type == newAlarm.type:
        self.alarms[i] = newAlarm
        return

  def isAlarmExist(self, alarmType):
    for alarm in self.alarms:
      if alarm.type == alarmType:
        return True

  def printAvailableAlarmTypes(self):
    for i, type in enumerate(alarm_types):
      print(f'{i} - {type}')
