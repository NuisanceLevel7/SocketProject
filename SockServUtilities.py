#!/usr/bin/python

import re,os,time,datetime,subprocess,sys
import os.path

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


