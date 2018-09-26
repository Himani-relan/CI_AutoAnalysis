#!/usr/bin/python3

import logging
from subprocess import Popen, PIPE

def execute(commands,f):
  f.write("=====================================\n")
  logging.info("Executing commands")
  for cmd in commands:
    try:
      f.write("Executing command: %s\n" % (cmd))
      process = Popen(cmd,  stdout = PIPE, stderr = PIPE, shell = True)
      (output, error) = process.communicate()
      f.write(output.decode("utf-8")+"\n")
      f.write("========================================\n")
    except Exception as e:
      logging.error(e)
      f.write(" Command Execution Failed\n")
