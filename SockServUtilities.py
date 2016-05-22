#!/usr/bin/python

import re,os,time,datetime,subprocess,sys
import os.path
import hashlib

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
        conn.close()
        print "\n\nGoodbye... " + data + "\n\n"
        break
      elif file_open:
        if '__END_SockServ_File__' in data:
          if len(data) > 21:
            entry = "Received a partial message with the EOT signal"
            logger.write_log(client_log, entry + "\n")
            savedata = data[0:len(data) - 21]
            bfh.write(savedata)
          bfh.close()
          # Check to see if we got a good file copy...
          # First compute the checksum and size of the received file
          f = Files()
          filestats = f.stat_file(filename)
          recv_filesize = filestats[1]
          recv_filechk = filestats[0]
          #
          # Now compare to expected values received from the client
          xfer_status = 'Success'
          if recv_filesize != int(filesize):
            xfer_status = 'Received File Size Mismatch'
            print "Expected ", int(filesize)
            print "Received ", recv_filesize
            logger.write_log(client_log, "Received file size mismatch\n")
          if str(recv_filechk) != filechk:
            xfer_status = 'Received File CheckSum Mismatch'
            print "Expected ", filechk
            print "Received ", str(recv_filechk)
            logger.write_log(client_log, "Received file checksum mismatch\n")
          reply = 'Transfer complete! Status =  ' + xfer_status + '...\n\n'
          conn.send(reply)
          conn.close()
          if xfer_status == 'Success':
            entry = "Transfer completed successfully"
            print entry
            logger.write_log(client_log, entry + "\n")
          else:
            entry = "Transfer Failed"
            print entry
            logger.write_log(client_log, entry + "\n")            
          break
        else:          
          bfh.write(data)
      elif 'SOCK_CLIENT_SENDING_FILE' in data.upper():
        print data
        fields = data.split(':')
        filename = "incoming/" + fields[1]
        filesize = fields[2].strip()
        filechk = fields[3].strip()
        filename = filename.strip()
        print "Receiving file " + filename + ' ' + str(filesize)
        bfh = open(filename,'wb')
        file_open = True
        
        conn.send('Prepared to receive ' + fields[1])

    #came out of loop
  
    
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

  def stat_file(self,fname):
    blocksize = 4096
    hash_sha = hashlib.sha256()
    f = open(fname, "rb")
    buf = f.read(blocksize)
    while 1:
      hash_sha.update(buf)
      buf = f.read(blocksize)
      if not buf:
        break    
    checksum =  hash_sha.hexdigest()
    filestat = os.stat(fname)
    filesize = filestat[6]
    return checksum,filesize

