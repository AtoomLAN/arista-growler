#!/usr/bin/env python

import CliParser, BasicCli, LazyMount, IpAddr

#------------------------------------------------------------------------------------
# The "growl" commands, in config mode.
#
#  growl login LINE
#  growl motd LINE
#------------------------------------------------------------------------------------

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

def setGrowlHost( mode, ipAddr, Pass, Level ):
   hosts = open("/persist/sys/growl","r")
   _hosts = []
   added = False
   for host in hosts:
      if host.rstrip() == "":
         continue
      config = host.split("\n")[0].split(",")
      if len(config) <= 1:
         continue
      if config[1] == ipAddr:
         _hosts.append("%s,%s,%s\n"%(Level,ipAddr,Pass))
         added = True
   if not added:
      _hosts.append("%s,%s,%s\n"%(Level,ipAddr,Pass))
   hosts = open("/persist/sys/growl","w")
   for host in _hosts:
      hosts.write("%s,%s,%s\n"%(Level,ipAddr,Pass))
   hosts.close()
   if added:
      print "Changed growl host %s"%(ipAddr)
   else:
      print "Added growl host %s"%(ipAddr)

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


def Plugin( entityManager ):
   global growlConfig
   growlConfig = ""
