#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from requests.auth import HTTPBasicAuth
from settings import userid, passcode,proxyDict

def trigger_thread_dump(landscape,processid,f):

  landscape = landscape.lower()
  for each in processid:
    f.write("===============================================================================\n")
    f.write("Generating thread dump for the process : %s \n" % (each))
    if landscape == 'trial':
      URL = 'https://monitoring.int.hanatrial.ondemand.com/monitoring/jmx/rest/' + each + '/operations/dumpStacktrace' 
      LOGURL = 'https://logviewer.int.hanatrial.ondemand.com/log/view/services/dispatcher/web/'
    elif landscape == 'eu1':
      URL = 'https://monitoring.int.hana.ondemand.com/monitoring/jmx/rest/' + each + '/operations/dumpStacktrace'
      LOGURL = 'https://logviewer.int.hana.ondemand.com/log/view/services/dispatcher/web/'
    else:
      URL = 'https://monitoring.int.' + landscape + 'hana.ondemand.com/monitoring/jmx/rest/' + each + '/operations/dumpStacktrace'
      LOGURL = 'https://logviewer.int.' + landscape + '.hana.ondemand.com/log/view/services/dispatcher/web/'

    try:
      resp = requests.post(URL, auth=HTTPBasicAuth(userid, passcode), proxies=proxyDict , headers = {'Content-Type': 'application/x-www-form-urlencoded'}, data = {'oname' : 'com.sap.js:name=Threading,type=Threading', 'params' : '[]'})
    except Exception as e:
      f.write("Error generating thread dump of process: %s\n" %(processid))
      f.write("Error: %s\n" % (e))
      return
    f.write("%s\n" % (resp.text))

  f.write("Thread dump is generated, download the logs from this location : %s\n" % (LOG_URL))

  return LOG_URL
  

if __name__ == "__main__":
  landscape = input("Enter landscape name")
  processid = input("Enter processid")
  trigger_thread_dump(landscape , processid, 'test.txt')

