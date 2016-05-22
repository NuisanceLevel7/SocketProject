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

f = Files()
filestats = f.stat_file(localfile)


print "Size = ", filestats[1]
print "Checksum = ", filestats[0]


host = 'nexus.viclab.org'
port = 8767                 

sockserv_log = 'cliest = os.stat("file.dat")nt.log'
 
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

s.send("SOCK_CLIENT_SENDING_FILE:" + remotefile + ':' + str(filestats[1]) + ':' + str(filestats[0]) )
print "REMOTE_HOST> " + s.recv(1024)

message = "Transferring " + localfile
logger.write_log(sockserv_log, message + "\n")
print message

f = open(localfile,'rb')

chunk = f.read(1024)
print 'Sending...'
while 1:
  s.send(chunk)
  chunk = f.read(1024)

  if not chunk:
    break
f.close()
print "Sending transfer complete signal"

s.send('__END_SockServ_File__')

print "Waiting for success ack from the server..."
#time.sleep(2)
final_ack = s.recv(1024)
print "REMOTE_HOST> " + final_ack
if 'Success' in final_ack:
  print "Data Transfer Completed Successfully"
else:
  print "There was an error transferring the file"
logger.write_log(sockserv_log,  final_ack + "\n")
# Cleanup
#
s.close
s.shutdown              

