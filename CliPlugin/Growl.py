#!/usr/bin/env python

import CliParser, BasicCli, LazyMount, IpAddr

#------------------------------------------------------------------------------------
# The "growl" commands, in config mode.
#
#  growl login LINE
#  growl motd LINE
#------------------------------------------------------------------------------------

#Create the command tokens
tokenGrowl = CliParser.KeywordRule( "growl", helpdesc="Configure the growls" )
GrowlHost = CliParser.TokenRule( matcher=IpAddr.IpAddrMatcher( "Growl host IP "
                                                                "address" ),name="ipAddr" )
GrowlPassword = CliParser.PatternRule( '.*',
                                        name="Pass",
                                        helpname='WORD',
                                        helpdesc='Growl password' )
GrowlLevel = CliParser.PatternRule( '[0-9]',
                                        name="Level",
                                        helpname='NUMBER',
                                        helpdesc='Minimal log level for sticky' )

growlConfig = None

#Adding/Changing hosts in the growl config
def setGrowlHost( mode, ipAddr, Pass, Level ):
   hosts = open("/persist/sys/growl","r")
   _hosts = []
   added = False
   for host in hosts:
      config = host.split("\n")[0].split(",")
      if len(config) <= 1:
         continue
      if config[1] == ipAddr:
         _hosts.append("%s,%s,%s\n"%(Level,ipAddr,Pass))
         added = True
      else:
         _hosts.append("%s\n"%(",".join(config)))
   if not added:
      _hosts.append("%s,%s,%s\n"%(Level,ipAddr,Pass))
   hosts = open("/persist/sys/growl","w")
   for host in _hosts:
      hosts.write(host)
   hosts.close()
   if added:
      print "Changed growl host %s"%(ipAddr)
   else:
      print "Added growl host %s"%(ipAddr)

#Removing hosts from the growl config
def clearGrowlHost( mode, ipAddr ):
   hosts = open("/persist/sys/growl","r")
   _hosts = []
   for _config in hosts:
      if _config.rstrip() == "":
         continue
      config = _config.split("\n")[0].split(",")
      if len(config) <= 1:
         continue
      if config[1] != ipAddr:
         _hosts.append(",".join(config))
   hosts.close()
   hosts = open("/persist/sys/growl","w")
   for host in _hosts:
      hosts.write("%s\n"%(host))
   hosts.close()
   print "Removed growl host %s"%(ipAddr)

BasicCli.GlobalConfigMode.addCommand(
   ( tokenGrowl, GrowlHost, GrowlPassword, GrowlLevel, setGrowlHost ) )

BasicCli.GlobalConfigMode.addCommand(
   ( BasicCli.noOrDefault, tokenGrowl, GrowlHost, clearGrowlHost ) )

#------------------------------------------------------------------------------------
# The "show growl" commands
#
#  show growl 
#------------------------------------------------------------------------------------
tokenShowGrowl = CliParser.KeywordRule( "growl", helpdesc="Show growl hosts connecten" )

#Show existing growl hosts
def showLoginGrowl( mode ):
   print "%-16s %-20s %-5s"%("Host","Password","Level")
   _config = open("/persist/sys/growl","r")
   for line in _config:
      line = line.rstrip()
      line = line.split(",")
      if len(line) <= 1:
         continue
      print "%-16s %-20s %-5s"%(line[1],line[2],line[0])

BasicCli.registerShowCommand( tokenShowGrowl, showLoginGrowl,
                              privileged=True )

ShowLion = CliParser.KeywordRule ("detail", helpdesc="show growl detail" )
tokenShowLion = CliParser.HiddenRule ( ShowLion )
def ohai( mode ):
   lion = """ GR0WLLLLLLLLL
                          ,%%%%%%%,
                        ,%%/\%%%%/\%,
                       ,%%%\c "" J/%%,
  %.                   %%%%/ d  b \%%%
  `%%.         __      %%%%    _  |%%%
   `%%      .-'  `"~--"`%%%%(=_Y_=)%%'
    //    .'     `.     `%%%%`\\7/%%%'____
   ((    /         ;      `%%%%%%%'____)))
   `.`--'         ,'   _,`-._____`-,
jgs  `\"\"\"`._____  `--,`          `)))
                `~"-)))"""
   print lion
BasicCli.registerShowCommand( tokenShowGrowl, tokenShowLion, ohai, privileged=True )

def Plugin( entityManager ):
   global growlConfig
   growlConfig = ""
