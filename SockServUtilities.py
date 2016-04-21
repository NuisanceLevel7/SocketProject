#!/usr/bin/python

import re,os,time,datetime,subprocess,sys
import os.path

class SocketConnectionServer:

  def __init__(self):
    self.status = ''    
  
  #Function for handling connections. This will be used to create threads
  def ConnectionHandler(self,conn,params):
  
    logger = Files()


    
    Dates = DateString()
    # Initial connect message to the client
    connection_num = params[0]
    remotehost = params[1]
    client_log = params[2]
  
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


class DateString:

  def __init__(self):
    self.yesterday = str(datetime.date.fromtimestamp(time.time() - (60*60*24) ).strftime("%Y-%m-%d"))
    self.today = str(datetime.date.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
    self.tomorrow = str(datetime.date.fromtimestamp(time.time() + (60*60*24) ).strftime("%Y-%m-%d"))
    self.now = str(time.strftime('%X %x %Z'))


class Files:

  def __init__(self):
    self.dir = ''
    self.readfile = []
    self.file_exists = 0

  def mkdir(self):
    if not os.path.isdir(self.dir):
      subprocess.call(["mkdir", self.dir])

  def write_file(self,filename,list):
    f = open(filename,'w')
    for line in list:
      f.write(line)
    f.close()

  def write_file_append(self,filename,list):
    f = open(filename,'a')
    for line in list:
      f.write(line)
    f.close()

  def write_log(self,logfile,logentry):
    f = open(logfile,'a')
    reportDate =  str(time.strftime("%x - %X"))
    f.write(reportDate + " :" + logentry)
    f.close()

  def read_file(self,filename):
    self.readfile = []
    self.file_exists = 1
    # Testing if file exists.
    if os.path.isfile(filename):
      try:
        f = open(filename,'r')
      except IOError:
        print "Failed opening ", filename
        sys.exit(2)
      for line in f:
        line = line.strip()
        self.readfile.append(line)
      f.close()
    else:
      # Set the file_exists flag in case caller cares.
      self.file_exists = 0


