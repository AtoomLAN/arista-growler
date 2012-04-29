"""
Author: Rudy Hardeman <zarya@gigafreak.net>
"""

from gntp import notifier
import time
import sys
import Tac, PyClient, subprocess, os

#Tail file function (eats file handle)
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

#Build growl connection function
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

#Connect to internal config database
pc = PyClient.PyClient("ar","Sysdb")
root = pc.root()

#Read out the switch hostname
hostname = root['ar']['Sysdb']['sys']['net']['config'].hostname

#Create the config file if it is not there
_temp = open("/persist/sys/growl","a")
_temp.close()

#Read all the lines comming from the logfile
for line in tail_f(open("/var/log/messages")):
    #Dont show log if there is only a cr on the line
    if line == "\n":
        continue

    #Remove the timestamp from the log line
    line = line.split(" ",4)[4]

    #Split in the service name and log entry
    (service,log) = line.split(":",1)

    #If it is a default syslog set level to 6
    try:
        level = log.split("-")[1]
    except:
        level = "6"

    #Open config for reading
    hosts = open("/persist/sys/growl","r")
    for _config in hosts:
        config = _config.split("\n")[0].split(",")
        
        #Try to connect to the growl host
        try:
            growl = growl_init(config)
        except:
            continue
        
        #Send growl message
        growl.notify(
            noteType = "New Messages",
            title = "%s: %s"%(hostname,service),
            description = log,
            sticky = level <= config[0],
            priority = 1,
        )
        del growl
    hosts.close() 
