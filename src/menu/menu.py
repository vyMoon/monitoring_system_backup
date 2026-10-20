from pathlib import Path
from alarm.alarm import Alarm
from alarm.alarm_types import alarm_types
from tools.tools import Tools
from alarm.alarm_service import AlarmService
from monitor.monitor import Monitor

menu_messages = {
  'menu': {
    'start': 'Welcome to our smal monitoring system',
    'finish': 'The program is finished. See you later.',
    'no_alarms': 'To start to work with the monitoring you need to create alarms',
    'cancel': 'Operation is interrupted',
    'cancel_message': 'Use ctrl + c to interrupt current operation'
  },
  'alarm': {
    'start_create': 'what type of alarm would you like to create',
    'existed': 'Alarm, {type} exists. Do you want to replace it?',
    'edit_type': 'You are going to change alarm with type: {type}. Provide new alarm limit',
    'delete': 'Which alarm would you like to delete?',
    'edit': 'Which alarm would you like to edit?',
  }
}

class Menu(Tools):
  alarms_file = Path.cwd() / 'alarms' / 'alarms.txt'
  alarmService = AlarmService()
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
          'fn': self.createAlarm
        },
        '1': {
          'text': 'Change existing alarm',
          'fn': self.editAlarm
        },
        '2': {
          'text': 'Delete alarm',
          'fn': self.deleteAlarm
        },
        '3': {
          'text': 'Start monitoring',
          'fn': self.monitorSystem
        }
      }

  def start(self):
    print(menu_messages['menu']['start'])
    print(menu_messages['menu']['cancel_message'])

    try:
      while True:
        if not self.alarmService.alarmCount:
          print(menu_messages['menu']['no_alarms'])
          self.createAlarm()
        else:
          self.showOptions()
    except KeyboardInterrupt:
      print(menu_messages['menu']['finish'])

  def showOptions(self):
    self.alarmService.printAlarms()

    choice = self.requestAnswer(self.options, 'What is next?')
    chosenOption = self.options[str(choice)]

    if 'fn' in chosenOption and callable(chosenOption.get('fn')): 
      chosenOption['fn']()
    else: print('not ready yet')
  
  def createAlarm(self):
    try:
      print(menu_messages['alarm']['start_create'])
      self.alarmService.printAvailableAlarmTypes()

      type = self.alarmService.getAlarmTypeByIndex(
        self.requestNumberBetween(self.alarmService.alarmTypesMaxIndex)
      )

      print('Set alarm value')
      target = self.requestNumberBetween(100)
      self.appendAlarm(type, target)
      self.saveAlarms()
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])

  def appendAlarm(self, type, target):
    if self.alarmService.isAlarmTypeExist(type):
      shouldAlarmBeReplaced = self.requestAnswer(
        self.yesNoOptions,
        menu_messages['alarm']['existed'].format(type=type)
      )
      if shouldAlarmBeReplaced:
        self.alarmService.replaceAlarm(Alarm(type, target))
    else:
      self.alarmService.extendAlarms([Alarm(type, target)])

  def editAlarm(self):
    try:
      idx = self.requestAnswer(
        self.alarmService.getAlarmsAsOptions(),
        menu_messages['alarm']['edit']
      )
      editedAlarm = self.alarmService.getAlarmByIndex(idx)
      print(menu_messages['alarm']['edit_type'].format(type=editedAlarm.type))
      target = self.requestNumberBetween(100)
      self.alarmService.replaceAlarm(
        Alarm(editedAlarm.type, target)
      )
      self.saveAlarms()
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])
      return

  def deleteAlarm(self):
    try:
      idx = self.requestAnswer(
        self.alarmService.getAlarmsAsOptions(),
        menu_messages['alarm']['delete']
      )
      self.alarmService.deleteAlarmByIndex(idx)
      self.saveAlarms()
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])
      return

  def monitorSystem(self):
    try:
      monitor = Monitor(self.alarms_file)
      monitor.startMonitor(self.getMonitoringTime())
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])
      return

  def getMonitoringTime(self):
    yes = self.requestAnswer(
      self.yesNoOptions,
      'Do you want to provide monitoring time? Otherwise it has no time limit.'
    )
    return self.requestNumber() if yes else None

  def checkAlarmsFile(self):
    if not self.alarms_file.exists():
      self.alarms_file.touch()

  def parseAlarms(self):
    with self.alarms_file.open('r') as file:
      data = file.readlines()
      if len(data):
        self.alarmService.extendAlarms(
          [Alarm(line.strip()) for line in data]
        )

  def saveAlarms(self):
    with self.alarms_file.open('w') as file:
      file.write(
        self.alarmService.getAlarmsSaveFormat()
      )

  def requestAnswer(self, options, message):
    print(message)
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
