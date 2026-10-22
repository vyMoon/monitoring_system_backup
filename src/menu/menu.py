from pathlib import Path
from alarm.alarm import Alarm
from alarm.alarm_types import alarm_types
from tools.tools import Tools
from alarm.alarm_service import AlarmService
from monitor.monitor import Monitor
from logger.logger import Logger

menu_messages = {
  'menu': {
    'start': 'Welcome to our smal monitoring system',
    'finish': 'The program is finished. See you later.',
    'no_alarms': 'To start to work with the monitoring you need to create alarms',
    'cancel': 'Operation is interrupted',
    'cancel_message': 'Use ctrl + c to interrupt current operation',
    'monitor_time': 'Do you want to provide monitoring time? Otherwise it has no time limit.',
  },
  'alarm': {
    'start_create': 'what type of alarm would you like to create',
    'existed': 'Alarm, {type} exists. Do you want to replace it?',
    'edit_type': 'You are going to change alarm with type: {type}. Provide new alarm limit',
    'delete': 'Which alarm would you like to delete?',
    'edit': 'Which alarm would you like to edit?',
  }
}

yesNoOptions = {
  '0': {
    'text': 'No',
  },
  '1': {
    'text': 'Yes',
  },
}

class Menu(Tools):
  alarms_file = Path.cwd() / 'alarms' / 'alarms.txt'
  logsPath = Path.cwd()
  alarmService = AlarmService()

  def __init__(self):
    self.logger = Logger(self.logsPath)
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

  def start(self, commands = None):
    if len(commands):
      self.startWithCommands(commands)
    else: self.startWithDialogs()

  def startWithCommands(self, commands):
    for c in commands:
      print(c[0])
      command = c[0].lower()
      if command == 'list':
        self.alarmService.printAlarms()
      elif command == 'alarm':
        alarmType = c[1]
        target = c[2]
        self.alarmService.saveAlarmFromConsole(alarmType, target)
        self.saveAlarms()
      elif command == 'delete':
        self.alarmService.deleteAlarmByType(c[1])
        self.saveAlarms()
      elif command == 'monitor' and c[1]:
        self.monitorSystem(c[1])
  
  def startWithDialogs(self):
    print(menu_messages['menu']['start'])
    print(menu_messages['menu']['cancel_message'])
    self.logger.log('Session stared')

    try:
      while True:
        if not self.alarmService.alarmCount:
          print(menu_messages['menu']['no_alarms'])
          self.logger.log('there is no alarms')
          self.createAlarm()
        else:
          self.showOptions()
    except KeyboardInterrupt:
      print(menu_messages['menu']['finish'])
    except Exception as e:
      self.logger.logPrefix('Error', f'{type(e).__name__}: {e}')
  
  def showOptions(self):
    self.alarmService.printAlarms()
    self.logger.logPrefix('Alarms', self.alarmService.getAlarmsSaveFormat())

    choice = self.requestAnswer(self.options, 'What is next?')
    chosenOption = self.options[str(choice)]

    if 'fn' in chosenOption and callable(chosenOption.get('fn')): 
      chosenOption['fn']()
    else: print('not ready yet')
  
  def createAlarm(self):
    self.logger.log('Alarm creation started')
    try:
      print(menu_messages['alarm']['start_create'])
      self.alarmService.printAvailableAlarmTypes()

      type = self.alarmService.getAlarmTypeByIndex(
        self.requestNumberBetween(self.alarmService.alarmTypesMaxIndex)
      )
      self.logger.logPrefix('Alarm creation', f'type chosen, type - {type}')

      print('Set alarm value')
      target = self.requestNumberBetween(100)
      self.logger.logPrefix('Alarm creation', f'Target chosen, target - {target}')
      self.appendAlarm(type, target)
      self.logger.logPrefix('Alarm creation', 'Alarm appended')
      self.saveAlarms()
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])
      self.logger.log('Session interrupted')

  def appendAlarm(self, type, target):
    if self.alarmService.isAlarmTypeExist(type):
      self.logger.logPrefix('Alarm creation', f'alarm with type {type} exists')
      shouldAlarmBeReplaced = self.requestAnswer(
        yesNoOptions,
        menu_messages['alarm']['existed'].format(type=type)
      )
      if shouldAlarmBeReplaced:
        self.logger.logPrefix('Alarm creation', f'user chose replace alar with type {type}')
        self.alarmService.replaceAlarm(Alarm(type, target))
    else:
      self.logger.logPrefix('Alarm creation', 'Alarm saving')
      self.alarmService.extendAlarms([Alarm(type, target)])

  def editAlarm(self):
    self.logger.logPrefix('Alarm editing', 'started')
    try:
      idx = self.requestAnswer(
        self.alarmService.getAlarmsAsOptions(),
        menu_messages['alarm']['edit']
      )
      editedAlarm = self.alarmService.getAlarmByIndex(idx)
      self.logger.logPrefix('Alarm editing', f'Edited alarm {editedAlarm}')
      print(menu_messages['alarm']['edit_type'].format(type=editedAlarm.type))
      target = self.requestNumberBetween(100)
      self.alarmService.replaceAlarm(
        Alarm(editedAlarm.type, target)
      )
      self.logger.logPrefix('Alarm editing', f'New target chosen target - {target}')
      self.saveAlarms()
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])
      return

  def deleteAlarm(self):
    self.logger.logPrefix('Alarm removal', 'started')
    try:
      idx = self.requestAnswer(
        self.alarmService.getAlarmsAsOptions(),
        menu_messages['alarm']['delete']
      )
      alarm = self.alarmService.getAlarmByIndex(idx)
      self.logger.logPrefix('Alarm removal', f'Chosen alarm - {alarm}')
      self.alarmService.deleteAlarmByIndex(idx)
      self.logger.logPrefix('Alarm removal', 'finished')
      self.saveAlarms()
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])
      return

  def monitorSystem(self, monitorTime = None):
    self.logger.logPrefix('Monitoring', 'started')
    try:
      monitor = Monitor(self.alarms_file, self.logger)
      monitor.startMonitor(monitorTime or self.getMonitoringTime())
    except KeyboardInterrupt:
      print(menu_messages['menu']['cancel'])
      return

  def getMonitoringTime(self):
    self.logger.logPrefix('Monitoring', 'User is offered to chose monitoring time')
    yes = self.requestAnswer(
      yesNoOptions,
      menu_messages['menu']['monitor_time']
    )
    print('Provide monitoring time in seconds')
    time = self.requestNumber() if yes else None
    self.logger.logPrefix('Monitoring', f'Monitoring time chosen, time - {time}')
    return time

  def checkAlarmsFile(self):
    if not self.alarms_file.exists():
      self.alarms_file.touch()
    self.logger.log('Alarm file status - ok')

  def parseAlarms(self):
    self.logger.log('Alarms is being retrieved')
    with self.alarms_file.open('r') as file:
      data = file.readlines()
      if len(data):
        self.logger.log(f'Alarms retrieved {data}')
        self.alarmService.extendAlarms(
          [Alarm(line.strip()) for line in data]
        )
      else: self.logger.log('There is no saved alarms')

  def saveAlarms(self):
    with self.alarms_file.open('w') as file:
      file.write(
        self.alarmService.getAlarmsSaveFormat()
      )
    self.logger.logPrefix('Alarm creation', 'Alarms saved')

  def requestAnswer(self, options, message):
    print(message)
    self.printOptions(options)
    maxIndex = self.getMaxIndex(options)
    chosen = self.requestNumberBetween(maxIndex)
    self.logger.log(f'Options chosen - {options[str(chosen)]['text']}')
    return chosen

  def printOptions(self, options):
    for i, option in options.items():
      print(f'{i} - {option['text']}')

  def getMaxIndex(self, collection):
    return max(
      [int(i) for i in collection.keys()]
    )
