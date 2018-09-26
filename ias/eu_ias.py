# -*- coding: utf-8 -*-
#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import IAS_EU_GID,IAS_EU_PRM,IAS_EU_SEC,IAS_EU_BAK,IAS_EU_CMDS
import sys
import threading
import logging
from commands_check import execute
from mailing import send_mail
from functions import get_current_status, get_location_details, get_outage_details,get_current_group_status


def get_status(mon):
  status = {}
  for monitor_id in mon:
    res = get_current_status(monitor_id)
    json_res = res.json()
    if json_res['message'] == 'success':
      if json_res['data']['status'] == 0:
        status[json_res['data']['name']] = "DOWN"
      else:
        status[json_res['data']['name']] = "UP"
    else:
      f.write("Could not fetch the status of monitor: %s \n" %(json_res['data']['name']))   
  return status


if __name__ == "__main__":
 
# Fetch the response of IAS EU group 
  file_name = "ias_eu_" + IAS_EU_GID
  f = open(file_name,"w")

  logging.basicConfig(filename = 'ias_eu.log', filemode='w', format= '%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' , level=logging.DEBUG )

  response = get_current_group_status(IAS_EU_GID)
  json_data = response.json()

  if json_data['message'] == 'success':
    if json_data['data']['status'] == 0:
      f.write("%s group status is down \n" %(json_data['data']['group_name']))
      logging.info("%s group status is down " , json_data['data']['group_name'])
      f.write("\n")

      down_list = []

      for each in json_data['data']['monitors']:
        if each['status'] == 0:
          down_list.append(each['name'])

      f.write("These IAS monitor(s) are down:\n")
      for item in down_list:
        f.write(item + "\n")

# Fetch outage details 
# Fetch location details
           
# Fetch the status of Primary DC – Converged Cloud  Rot 
      f.write("=============================================\n")
      f.write("Checking the status of Primary DC – Converged Cloud Rot...\n")
      primary_status = get_status(IAS_EU_PRM)
      for k,v in primary_status.items():
        f.write(k+": "+v)
        f.write("\n")


# Check the current status of Secondary DCs' monitor
      f.write("=============================================\n")
      f.write("Checking the status of Secondary DC - Monsoon 2 Rot...\n")
      secondary_status = get_status(IAS_EU_SEC)
      for k,v in secondary_status.items():
        f.write(k+": "+v)
        f.write("\n")

# Check the current status of Backup DCs' monitor
      f.write("=============================================\n")
      f.write("Checking the status of Backup DC - Converged Cloud Amsterdam ...\n")
      backup_status = get_status(IAS_EU_BAK)
      for k,v in backup_status.items():
        f.write(k+": "+v)
        f.write("\n")

# Executing commands
      execute(IAS_EU_CMDS,f)

      f.close()

# Send an email with Bridge Template and results file
      if (os.path.exists("eu_status_file.txt")) and (os.path.getsize("eu_status_file.txt")) > 0:
        sf = open("eu_status_file.txt", "r")
        sf_content = sf.read().rstrip('\n')
        if (sf_content == '1') and (json_data['data']['status'] == 0):
          subject = json_data['data']['group_name'] + " group status is down"
          send_mail('EU',subject, down_list,file_name, primary_status , secondary_status, backup_status)
        else:
          logging.info("Not sending email")

      sf = open("eu_status_file.txt", "w")
      sf.write("%s" % (json_data['data']['status']))
      sf.close()

    else:
      sf = open("eu_status_file.txt", "w")
      sf.write("%s" % (json_data['data']['status']))
      sf.close()
      logging.info("%s group status is up " , json_data['data']['group_name'])
      sys.exit()
  else:
    logging.error("API response is not correct, message: %s", json_data['message'])
