#!/usr/bin/python

import socket
import sys
from thread import *
import re,os,time,datetime,subprocess
import os.path
from SockServUtilities import DateString
from SockServUtilities import Files

import socket      

if len(sys.argv) < 3:
  print "USAGE sock_client.py LOCAL_FILE REMOTE_FILE"
  sys.exit()
localfile = sys.argv[1]
remotefile = sys.argv[2]
  
s = socket.socket()        
host = 'nexus.viclab.org'
port = 8767                 

s.connect((host, port))
print "REMOTE_HOST> " + s.recv(1024)

s.send("SOCK_CLIENT_SENDING_FILE: " + remotefile)
print "REMOTE_HOST> " + s.recv(1024)

f = open(localfile,'rb')
print 'Begin Transmission...'
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

# Cleanup
#
s.close
s.shutdown              

