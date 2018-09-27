#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from requests.auth import HTTPBasicAuth
import logging
from settings import HEL_GID,subaccount,userid, passcode
import threading
from functions import get_current_group_status,get_location_details, get_outage_details
from check_metrics import app_vm_metrics, static_host_metrics
from thread_dump import trigger_thread_dump
from scenario import designtime_scenario,getappurl
from send_mail import send_mail


def get_downtime_info(mon_id, name, landscape_name):

  filename = "dispatcher_" + landscape_name
  f = open(filename , "w")
  f.write("%s is down \n" % (name))

  final_result = {}
# Fetch Outage details
  get_outage_details(mon_id , f)

# Fetch the current metrics of dispatcher application. Function will return the process id for which metrics are critical
  processid = app_vm_metrics(landscape_name,'services','dispatcher',f)

# Trigger thread dump of the failed dispatcher processes
  if not processid:
    f.write("===========================================================================\n")
    f.write("Current metrics of all the processes are OK, hence thread dump is not generated\n")
  else:
    for process in processid:
      logurl = trigger_thread_dump(landscape_name, process,f)
# Fetch the status of MaxdB used by Helium
  stat = static_host_metrics(landscape_name,"HeliumDB", f)
  if not stat:
    HeliumDBStatus = "OK"
  else:
    HeliumDBStatus = "CRITICAL"
  final_result['HeliumDBStatus'] = HeliumDBStatus

# Fetch the status of DomainDb
  status = static_host_metrics(landscape_name,"Domaindb",f)
  if not status:
    DomainDBStatus = "OK"
  else:
    DomainDBStatus = "CRITICAL"
  final_result['DomainDBStatus'] = DomainDBStatus

# Create/Activate/Start HTML5 sample application ( To test Design Time scenario)
  f.write("==============================================================\n")
  f.write("Test Design Time scenario : Create/Activate/Start HTML5 application.\n")
  result = designtime_scenario(landscape_name,f,subaccount)
  if not result:
    f.write("Design Time scenario failed in %s landscape\n" %(landscape_name))
    design_result = "FAIL"
    appname = ""
  else:
    f.write("Design time scenario succeeded\n")
    design_result = "PASS"
    appname = result
  final_result['DesignTimeScenario_Result'] = design_result

# Get the application URL which needs to be accessed & Test the runtime scenario
  f.write("==============================================================\n")
  f.write("Test Runtime scenario : Access the HTML5 application\n")
  if not appname:
    appname = "testapp"
    f.write("Taking already existing app :%s to check the runtime scenario\n" %(appname))

  appurl = getappurl(landscape_name, subaccount, appname, f)
  if not appurl:
    f.write("Unable to fetch the application URL of %s \n" %(appname))
    f.write("Runtime scenario can't be tested \n")
    runtime_result = "FAIL"
  else:
    try:
      resp = requests.get(appurl, auth=HTTPBasicAuth(userid, passcode))
    except Exception as e:
      f.write("Error while calling the Application URL :%s\n" %(appurl))
      f.write("Error :%s\n" %(e))
      runtime_result = "FAIL"
      
    if resp.status_code == 200:
      f.write("Application URL is accessible\n")
      f.write("Runtime scenario succeeded\n")
      runtime_result = "PASS"
    else:
      f.write("Not able to access HTML5 test application: %s \n" % (appname))
      f.write("Runtime scenario failed\n")
      runtime_result = "FAIL"
   
  final_result['RuntimeScenarioResult'] = runtime_result
  f.close()

# Send an email
  subject = name + "is down"
  sf = open(filename , "r")
  send_mail(landscape_name, subject, final_result, filename)
  sf.close()



if __name__ == '__main__':

  logging.basicConfig(filename = 'dispatcher.log', filemode='w', format= '%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' , level=logging.DEBUG )

# Fetch the status of HCP Application Runtime group status
  logging.info("Fetching the current status of HTML5 Application Runtime Group : %s ", HEL_GID)
  response = get_current_group_status(HEL_GID)
  json_data = response.json()

  if json_data['message'] == 'success':
    if json_data['data']['status'] == 0:
      logging.info("HTML5 Application Runtime Group Status is down")
      t = []

# Get the down monitors in the group
      for each in json_data['data']['monitors']:
        if each['status'] == 0:
          l = each['name'].split(" ")
          landscape_name = l[0]
          statusfile = landscape_name + "_status.txt"
          with open(statusfile, 'r') as sf:
            sf_content = sf.read().rstrip('\n')

          if (sf_content == '1'):
            with open(statusfile , 'w') as sf:
              sf.write(str(each['status']))
            thread = threading.Thread(target = get_downtime_info , args = (each['monitor_id'], each['name'], landscape_name) , name="%s" %(each['name']))
            t.append(thread)
            logging.info("Starting thread : %s ", thread.getName()) 
            thread.start()
          else:
            logging.info("Email has already been sent for %s , hence not sending mail again"  % (landscape_name))

      [x.join() for x in t]
    else:
      logging.info("HTML 5 Application Runtime Group status is UP")
      for each in json_data['data']['monitors']:
        l = each['name'].split(" ")
        landscape_name = l[0]
        statusfile = landscape_name + "_status.txt"
        with open(statusfile, 'w') as sf:
      sys.exit()
  else:
    logging.error("API response is not correct, message: %s", json_data['message'])
