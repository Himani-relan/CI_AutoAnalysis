# -*- coding: utf-8 -*-
#!/usr/bin/python3


import requests
import sys
import logging
from settings import BASE_URL,header

#Function to fetch outage details
def get_outage_details(monitor_id,f):
  f.write("======================================\n")
  f.write("Fetching the Outage Details:\n")
  try:
    resp = requests.get(BASE_URL+"reports/outage/"+monitor_id , headers = header, params = {'period': 5 })
  except Exception as e:
    f.write(" Error occurred while calling API for fetching details of an outage\n")
    f.write("Error: %s\n" % (e))
    sys.exit()

  json_result= resp.json()

  if json_result['message'] == 'success':
    for outage in json_result['data']['outage_details']:
      for list in outage['outages']:
        f.write("Start Time : %s\n" % (list['start_time']))
        f.write("End Time : %s\n" % (list['end_time']))
        f.write("Duration : %s\n" % (list['duration']))
        f.write("Reason : %s\n" % (list['reason']))
        break

  else:
    f.write("Error while fetching API response, message: %s\n" % (json_result['message']))

# Function to fetch current status of a monitor
def get_current_status(monitor_id):
  try:
    logging.info("Fetching the current status of a monitor: %s", monitor_id)
    response = requests.get(BASE_URL + "current_status/"+ monitor_id , headers = header)
    return response
  except Exception as e:
    logging.error("Error occurred while fetching current status of monitor : %s", monitor_id)
    logging.error("Error : %s ", e)
    sys.exit()

#Function to fetch the location details from where the monitor is down
def get_location_details(loc,f):
  f.write("======================================\n")
  f.write("Fetching the locations from where the monitor is down:\n")
  for each in loc:
    if each['status'] == 1:
      f.write(each['location_name']+"\n")

#Function to fetch the current status of a monitor group
def get_current_group_status(group_id):
  try:
    logging.info("Fetching the current status of a monitor group : %s" , group_id)
    res = requests.get(BASE_URL + "current_status/group/"+ group_id , headers = header)
    return res
  except Exception as e:
    logging.error("Error occurred while fetching status of monitor group: %s", group_id)
    logging.error("Error: %s " ,e)
    sys.exit()

