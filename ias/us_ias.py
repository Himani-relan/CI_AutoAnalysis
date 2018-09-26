# -*- coding: utf-8 -*-
#!/usr/bin/python3


import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from settings import IAS_US_GID,IAS_US_PRM,IAS_US_SEC,IAS_US_CMDS
import sys
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
 
# Fetch the response of IAS US group 
  file_name = "ias_us_" + IAS_US_GID
  f = open(file_name,"w")

  logging.basicConfig(filename = 'ias_us.log', filemode='w', format= '%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p' , level=logging.DEBUG )

  response = get_current_group_status(IAS_US_GID)
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

           
# Fetch the status of Primary DC – Converged Cloud
      f.write("=============================================\n")
      f.write("Checking the status of Primary DC – Converged Cloud...\n")
      primary_status = get_status(IAS_US_PRM)
      for k,v in primary_status.items():
        f.write(k+": "+v)
        f.write("\n")


#Check the current status of Secondary DCs' monitor
      f.write("=============================================\n")
      f.write("Checking the status of Secondary DC - Toronto ...\n")
      secondary_status = get_status(IAS_US_SEC)
      for k,v in secondary_status.items():
        f.write(k+": "+v)
        f.write("\n")

#Executing commands
      execute(IAS_US_CMDS,f)

      f.close()

#Send an email with Bridge Template and results file
      if (os.path.exists("us_status_file.txt")) and (os.path.getsize("us_status_file.txt")) > 0: 
        sf = open("us_status_file.txt", "r")
        sf_content = sf.read().rstrip('\n')
        if (sf_content == '1') and (json_data['data']['status'] == 0):
          subject = json_data['data']['group_name'] + " group status is down"
          send_mail('US',subject, down_list,file_name, primary_status , secondary_status)
        else:
          logging.info("Not sending email")
      
      sf = open("us_status_file.txt", "w")
      sf.write("%s" % (json_data['data']['status']))
      sf.close()

    else:
      sf = open("us_status_file.txt", "w")
      sf.write("%s" % (json_data['data']['status']))
      sf.close()
      logging.info("%s group status is up " , json_data['data']['group_name'])
      sys.exit()
  else:
    logging.error("API response is not correct, message: %s", json_data['message'])
