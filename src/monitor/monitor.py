import psutil
from pathlib import Path
from alarm.alarm import Alarm
# Monitor
# hostar psutil modul 
# hostar logger
# run loop som monitorerar systemet

# m = Monitor([larm1, larm2, larm3])
# tar min 1, max 3 larmar av olika typer annars rise error
# ser till att larmar är av olika type  annars rise error
# kör loop och kollar på parametrarna Alarm. check()
# loggar och printar med hjälp av logger
# Larm.check -> true \ false
# if larm true -> print och log error
# __str__, __ len__ methods

class Monitor:
  def __init__(self, alarm_path, monitor_time):
    self.alarm_path = alarm_path
    self.monitor_time = monitor_time
    self.getAlarms()

  def getAlarms(self):
    with self.alarm_path.open('r') as file:
      data = file.readlines()
      self.alarms = [Alarm(line.strip()) for line in data]

  
  def startMonitor(self):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    print(cpu, ram, disk)


# m = Monitor(
#   (Path.cwd() / 'alarms' / 'alarms.txt' ),
#   10
# )
# m.startMonitor()
