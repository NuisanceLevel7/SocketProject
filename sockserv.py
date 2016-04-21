#!/usr/bin/python

# Socket based file transfer server
# Copyright Vic Engle 2016 All rights reserved
#
#

from thread import *
import re,os,time,datetime,subprocess,socket,sys
from SockServUtilities import DateString
from SockServUtilities import Files
from SockServUtilities import SocketConnectionServer
from optparse import OptionParser

# Parse command line options...
parser = OptionParser()
parser.add_option("-p", "--port", dest="port",
                  help="Port on remote host for connection")
(options, args) = parser.parse_args()                  


# Set a few variables...
HOST = ''
PORT = 8767
WORKERS = 10
sockserv_log = 'sockserv.log'
client_log = 'connection_handler.log'
pid = os.getpid()
logger = Files()
if options.port:
  PORT = int(options.port)

logger.write_log(sockserv_log, "Socket Server Starting Up. PID=" + str(pid) + "\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# Bind socket to local host and port, but catch exceptions
try:
  s.bind((HOST, PORT))
except socket.error as msg:
  print 'Unable to bind to port: ' + str(PORT) + "\n\nError message from the OS...\n\n" + str(msg[0]) + ' Message ' + msg[1] + "\n\nExiting..."
  sys.exit(10)

print 'Socket bind complete'
logger.write_log(sockserv_log, "Socket Server Bind Okay, Listening Socket open on Port-" + str(PORT) + "\n")
# Start listening on socket.
s.listen(WORKERS)
print 'Socket now listening on port, ' + str(PORT)

# Now listen for client connection on the bind port and pass them off workers.
# We create one worker object and use the threads library to run parallel instances
worker = SocketConnectionServer()
conn_count = 0
while 1:
  #wait to accept a connection - blocking call
  conn, addr = s.accept()
  print 'Connected with ' + addr[0] + ':' + str(addr[1])
  conn_count += 1
  #
  # This is a tuple of arguments to pass to client connection handler
  #
  client_handler_args = str(conn_count), str(addr[0]), client_log
  #
  # Start new thread takes 1st argument as a function name to be run, second is a tuple of arguments to the function.
  # In this case, the function is a a method from the class imported from SocketConnectionServer
  # and the tuple is in this format: tuple(connection_object, tuple(connection#, remote_IP, client_log))
  start_new_thread(worker.ConnectionHandler ,(conn,client_handler_args))

s.close()

