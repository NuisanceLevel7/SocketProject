#!/usr/bin/python

# Socket based file transfer server
# Copyright Vic Engle 2016 All rights reserved
#
#
import socket
import sys
from thread import *
import re,os,time,datetime,subprocess
import os.path
from SockServUtilities import DateString
from SockServUtilities import Files




HOST = ''
PORT = 8767
WORKERS = 10
sockserv_log = 'sockserv.log'
client_log = 'clients.log'
pid = os.getpid()
logger = Files()

logger.write_log(sockserv_log, "Socket Server Starting Up. PID=" + str(pid) + "\n")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
  s.bind((HOST, PORT))
except socket.error as msg:
  print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
  sys.exit()

print 'Socket bind complete'
logger.write_log(sockserv_log, "Socket Server Bind Okay, Listening Socket open on Port-" + str(PORT) + "\n")
#Start listening on socket.
s.listen(WORKERS)
print 'Socket now listening on port, ' + str(PORT)

#Function for handling connections. This will be used to create threads
def ConnectionHandler(conn,params):

  global welcome
  Dates = DateString()
  # Initial connect message to the client
  connection_num = params[0]
  remotehost = params[1]
  
  pid = os.getpid()
  
  logger.write_log(client_log, "PID " + str(pid) + " Handling Conn# " + connection_num + "\n")
  logger.write_log(client_log, "Conn# " + str(connection_num) + " talking to remote host, " + str(remotehost) + "\n")


  conn.send('Connection established. Ready to receive')
  connection_num = params[0]
  
  file_open = False	
  # Handle client file transfer
  while True:
    
    #Receiving from client
    data = conn.recv(1024)
    if not data:
      reply = 'Disconnecting from IP addr ' + remotehost + '...\n\n'
      conn.sendall(reply)
      print "Sending disconnect notice to Client"
      conn.close()
      print "\n\nGoodbye... " + data + "\n\n"
      break
    elif file_open:
	  bfh.write(data)
    elif 'SOCK_CLIENT_SENDING_FILE' in data.upper():
      fields = data.split()
      filename = "incoming/" + fields[1]
      filename = filename.strip()
      bfh = open(filename,'wb')
      file_open = True
      print "Sending: Prepared to receive"
      conn.send('Prepared to receive ' + fields[1])
  #came out of loop
  
  bfh.close()
  conn.close()

#now keep talking with the client
conn_count = 0
while 1:
  #wait to accept a connection - blocking call
  conn, addr = s.accept()
  print 'Connected with ' + addr[0] + ':' + str(addr[1])
  conn_count += 1
  #
  # This is a tuple of arguments to pass to client connection handler
  #
  client_handler_args = str(conn_count), str(addr[0])
  #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
  start_new_thread(ConnectionHandler ,(conn,client_handler_args))

s.close()

