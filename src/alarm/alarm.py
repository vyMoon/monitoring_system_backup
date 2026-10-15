import re
from alarm_types import alarm_types

# Alarm
# Innehåler imformation om  alarmet
# disk, ram, cpu
# har check method som tar värde och jämför med värde som fik

# Alarm(type, target) Alarm('cpu': string, 500:int)
# ser till att type är sträng och
# target är percent from 0 ? to 100 integer(float??) annars rise error
# types = 'cpu' \ 'ram' \ disk

# check method kollar på om argumenten är lägre högre elle lika med target
# om lägre returnera false annars true

class Alarm:
  name = 'Alarm'
  pattern = r'^Alarm - type: (cpu|disc|ram), target: \d+$'

  def __init__(self, alarm_type, target=None):
    if self.isParsAble(alarm_type):
      info = self.parseAlarm(alarm_type)
      alarm_type = info['type']
      target = info['target']

    self.validateType(alarm_type)
    self.validateTarget(target)
    self.type = alarm_type
    self.target = target

  def __str__(self):
    return f'{self.name} - type: {self.type}, target: {self.target}'

  def validateType(self, alarm_type):
    if type(alarm_type) != str:
      raise ValueError('Alarm type must be a string')
    if alarm_type not in alarm_types:
      raise ValueError(
        'Aalarm type must be "disc" "ram" or "cpu"'
      )
  
    return True

  def validateTarget(self, target):
    self.validateTargetType(target)
    if 0 > target or target > 100:
      raise ValueError('Target must be from 0 to 100')
    return True

  def validateTargetType(self, target):
    if type(target) is not int and type(target) is not float:
      raise ValueError(
        'Target must be a integer or float'
      )
    return True
  
  def isBreached(self, value):
    self.validateTargetType(value)
    return value >= self.target

  def isParsAble(self, stringified_alarm):
    return bool(re.fullmatch(self.pattern, stringified_alarm))

  def parseAlarm(self, stringified_alarm):
    match = re.search(r"type: *(cpu|disc|ram)", stringified_alarm)
    if match:
      alarmType = match.group(1)
    match = re.search(r"target: *(\d+)", stringified_alarm)
    if match:
      target = match.group(1)

    return {
      'type': alarmType,
      'target': int(target)
    }


a = Alarm('Alarm - type: disc, target: 100')
print(a)