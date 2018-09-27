#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from requests.auth import HTTPBasicAuth
import yaml
from urllib.parse import unquote
from settings import userid,passcode,proxyDict

# Method to fetch the current metrics of application VM's
def app_vm_metrics(landscape,account,application,f):
  f.write("===============================================\n")
  f.write("Fetching the current metrics of %s processes\n" % (application))
  landscape = landscape.lower()
  if landscape == "trial":
    URL = "https://api.hanatrial.ondemand.com/monitoring/v1/accounts/"+ account + "/apps/" + application + "/metrics"
  else:
    URL = "https://api." + landscape + ".hana.ondemand.com/monitoring/v1/accounts/"+ account + "/apps/" + application + "/metrics"

  try:
    resp = requests.get(URL, auth=HTTPBasicAuth(userid, passcode))
  except Exception as e:
    f.write(" Unable to retreive the current status of %s, Failure in calling API\n" % (application))
    f.write("Error: %s " % (e))
    sys.exit()

  if resp.status_code == 200:
    json_data=resp.json()

    processes = []
    if json_data[0]['state'] == "Ok":
      f.write("All metrics of %s are OK\n" % (application))
    else:
      for each in json_data[0]['processes']:
        if each['state'] == "Ok" :
          continue
        else:
          processes.append(each['process'])
          f.write("\n")
          f.write("=======================================================\n")
          f.write("Process : %s State: %s\n" % (each['process'], each['state']))
          for metric in each['metrics']:
            if metric['state'] == "Ok":
              continue
            else:
              f.write("%s == %s : %s\n" % (metric['name'] , metric['state'], metric['output']))
    return processes
  else:
    f.write("Fetching the current metrics by calling API is failing\n")

# Method to fetch the current metrics of static hosts
def static_host_metrics(landscape,statichosts,f):
  f.write("===============================================\n")
  f.write("Fetching the current metrics of %s\n" % (statichosts))

  with open("info.yml",'r') as ymlfile:
    landscape = landscape.lower()
    cfg=yaml.load(ymlfile)

    statichost = cfg[landscape][statichosts]
  flag = 0

  for host in statichost:
    count = 0
    f.write("==========================================\n")
    f.write(host+'\n')
    if landscape == "trial":
      URL= "https://monitoring.int.hanatrial.ondemand.com/monitoring/detailedmetrics/staticservice/" + host
    elif landscape == "eu1":
      URL= "https://monitoring.int.hana.ondemand.com/monitoring/detailedmetrics/staticservice/" + host
    else:
      URL= "https://monitoring.int."+ landscape +".hana.ondemand.com/monitoring/detailedmetrics/staticservice/" + host

    PATTERN = "CRITICAL"
    try:
      resp = requests.get(URL, auth=HTTPBasicAuth(userid, passcode) , proxies=proxyDict)
    except Exception as e:
      f.write(" Unable to retreive the current status of Static Hosts, Failure in calling API\n")
      f.write(" Error : %s " % (e))
      return
    json_data=resp.json()
    host = unquote(host)

    for each in json_data[host]:
      if each['output'].find(PATTERN) != -1:
        f.write("%s =  %s\n" % (each['description'], each['output']))
        count = count+1

    if count == 0:
      f.write("There are no critical metrics in %s\n" % (host))
    else:
      flag =  flag+1
  return flag
