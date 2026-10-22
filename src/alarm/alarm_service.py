from alarm.alarm_types import alarm_types
from alarm import Alarm

class AlarmService:
  def __init__(self, alarmMax = 3, alarmTypes = alarm_types):
    self.alarmMax = alarmMax
    self.alarmTypes = alarmTypes
    self.alarms = []

  @property
  def alarmTypesMaxIndex(self):
    return len(self.alarmTypes) - 1

  @property
  def alarmCount(self):
    return len(self.alarms)

  def getAlarms(self):
    return self.alarms.copy()
  
  def extendAlarms(self, alarms):
    self.alarms.extend(alarms)
  
  def printAvailableAlarmTypes(self):
    for i, type in enumerate(self.alarmTypes):
      print(f'{i} - {type}')

  def getAlarmTypeByIndex(self, idx):
    return self.alarmTypes[idx]

  def isAlarmTypeExist(self, alarmType):
    for alarm in self.alarms:
      if alarm.type == alarmType:
        return True
    return False

  def saveAlarmFromConsole(self, type, target):
    alarm = Alarm(type, target)
    if self.isAlarmTypeExist(type):
      self.replaceAlarm(alarm)
    else: self.extendAlarms([alarm])

  def replaceAlarm(self, newAlarm):
    for i, alarm in enumerate(self.alarms):
      if alarm.type == newAlarm.type:
        self.alarms[i] = newAlarm
        return

  def deleteAlarmByIndex(self, idx):
    self.alarms.pop(idx)

  def deleteAlarmByType(self, alarmType):
    idx = self.getAlarmIndexByType(alarmType)

    if idx != False: self.deleteAlarmByIndex(idx)

  def getAlarmIndexByType(self, alarmType):
    for i, a in enumerate(self.alarms):
      if a.type == alarmType:
        return i
    return False
  
  def getAlarmsAsOptions(self):
    options = {}
    for i, alarm in enumerate(self.alarms):
      options[str(i)] = {
        'text': str(alarm)
      }
    return options

  def printAlarms(self):
    if not self.alarmCount:
      return print('There is no alarms in the system')
    print('\nThe list of alarms')

    for alarm in self.alarms:
      print(alarm)

  def getAlarmByIndex(self, idx):
    return self.alarms[idx]

  def getAlarmsSaveFormat(self):
    return ('\n'.join([str(a) for a in self.alarms])
      if len(self.alarms)
      else ''
    )
