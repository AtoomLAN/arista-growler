from gntp import notifier
import time
import sys
import Tac, PyClient, subprocess, os

 
def tail_f(file):
  interval = 1.0
  file.seek( int(-1), 2 )
  while True:
    where = file.tell()
    line = file.readline()
    if not line:
      time.sleep(interval)
      file.seek(where)
    else:
      yield line

def growl_init(config):
    growl = notifier.GrowlNotifier(
        applicationName = "Arista %s"%(hostname),
        notifications = ["New Updates","New Messages"],
        defaultNotifications = ["New Messages"],
        hostname = config[1],
        password = config[2]
    )
    growl.register()
    return growl

pc = PyClient.PyClient("ar","Sysdb")
root = pc.root()

hostname = root['ar']['Sysdb']['sys']['net']['config'].hostname

_temp = open("/persist/sys/growl","a")
_temp.close()

#Apr 28 18:51:40 7048TOP Fru: %FRU-6-FAN_REMOVED: Fan tray 5 has been removed

for line in tail_f(open("/var/log/messages")):
    if line == "\n":
        continue
    line = line.split(" ",4)[4]
    (service,log) = line.split(":",1)
    try:
        level = log.split("-")[1]
    except:
        level = "6"
    hosts = open("/persist/sys/growl","r")
    for _config in hosts:
        config = _config.split("\n")[0].split(",")
        try:
            growl = growl_init(config)
        except:
            continue
        
        growl.notify(
            noteType = "New Messages",
            title = "%s: %s"%(hostname,service),
            description = log,
            sticky = level <= config[0],
            priority = 1,
        )
        del growl
    hosts.close() 
