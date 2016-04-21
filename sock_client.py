#!/usr/bin/python


# Socket File Transfer Client
# Copyright 2016 by Vic Engle, all rights reserved

import re,os,time,datetime,subprocess,sys,socket
from SockServUtilities import DateString
from SockServUtilities import Files
from optparse import OptionParser
from thread import *

parser = OptionParser()

parser.add_option("-l", "--localfile", dest="localfile",
                  help="Name of Local FILE __REQUIRED__")
                  
parser.add_option("-r", "--remotefile", dest="remotefile",
                  help="Name for Remote File")

parser.add_option("-p", "--port", dest="port",
                  help="Port on remote host for connection")
                  
parser.add_option("-s", "--server", dest="server",
                  help="Name for Remote server")


(options, args) = parser.parse_args()

if not options.localfile:
  print "Woops, you didn't tell me a local file name. tsk tsk. Exiting..."
  print "Run the program with -h for help"
  sys.exit(1)

if not options.remotefile:
  remotefile = os.path.basename(options.localfile)
else:
  remotefile =  options.remotefile

 
localfile =  options.localfile

host = 'nexus.viclab.org'
port = 8767                 

sockserv_log = 'client.log'
 
if options.port:
  port = int(options.port)

if options.server:
  host = options.server
 
s = socket.socket()        
logger = Files()

message = "Attempting to connect to " + host + " on port# " + str(port)
logger.write_log(sockserv_log, message + "\n")
print message

try:
  s.connect((host, port))
except socket.error as msg:
  print 'Connection failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
  sys.exit()

logger.write_log(sockserv_log, "Connected!\n")  
print "Connected!"

print "REMOTE_HOST> " + s.recv(1024)

s.send("SOCK_CLIENT_SENDING_FILE: " + remotefile)
print "REMOTE_HOST> " + s.recv(1024)

message = "Transferring " + localfile
logger.write_log(sockserv_log, message + "\n")
print message

f = open(localfile,'rb')

chunk = f.read(1024)

while 1:
  print 'Sending...'
  s.send(chunk)
  chunk = f.read(1024)
  if not chunk:
    break
f.close()

s.send('')
print "Data Transfer Complete"
logger.write_log(sockserv_log,  "File Transfer Completed.\n")
# Cleanup
#
s.close
s.shutdown              

