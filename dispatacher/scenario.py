#!/usr/bin/python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from requests.auth import HTTPBasicAuth
from settings import userid, passcode, html5testapp, html5testrepo


# DesignTime Scenarios ( Create, activate, start HTML5 application)
def designtime_scenario(landscape,f, account):
  landscape = landscape.lower()
  if landscape == "trial":
    BASEURL = "https://dispatcher.hanatrial.ondemand.com/hcproxy/b/api/accounts/"
  elif landscape == "eu1":
    BASEURL = "https://dispatcher.hana.ondemand.com/hcproxy/b/api/accounts/"
  else:
    BASEURL = "https://dispatcher." + landscape + ".hana.ondemand.com/hcproxy/b/api/accounts/"

  with requests.Session() as c:
    URL = BASEURL + account + "/applications/"
# Fetch CSRF-TOKEN using get request to list all applications in an account
    try:
      resp = c.get(URL, auth=HTTPBasicAuth(userid,passcode), headers = {'X-CSRF-TOKEN' : 'FETCH'})
    except Exception as e:
      f.write("Error while calling API to fetch applications in account: %s\n" %(account))
      f.write("No further POST requests can be made as X-CSRF-TOKEN can't be fetched\n")
      f.write("Error: %s\n" %(e))
      return
    if resp.status_code == 200:
      respheader = resp.headers
      try:
        csrftoken = respheader['X-CSRF-Token']
      except Exception as e:
        f.write("No further POST requests can be made as X-CSRF-TOKEN can't be fetched\n")
        return
    else:
      f.write("No further POST requests can be made as X-CSRF-TOKEN can't be fetched\n")
      f.write("Status Code: %s , Output: %s\n" % (resp.status_code , resp.text))
      return

# Create an application
    create_payload = "{\"name\":\"" + html5testapp + "\", \"repository\" :\"" + html5testrepo + "\" }"
    try:
      response = c.post(URL, auth=HTTPBasicAuth(userid,passcode), headers = {'X-CSRF-Token' : csrftoken } ,data = create_payload)
    except Exception as e:
      f.write("Error while calling API to create an application\n")
      f.write("Error: %s\n" %(e))
      return

    if response.status_code == 201:
      f.write("Test application: %s created successfully\n" %(html5testapp))
    else:
      f.write("Application creation failed\n")
      f.write("Status Code : %s , Output : %s\n" % (response.status_code , response.text))
      return

# Activate version of an application
    activate_payload = "\"ACTIVATE\""
    ACTIVATE_URL = URL + html5testapp + "/versions/1/action"
    try:
      res = c.post(ACTIVATE_URL, auth=HTTPBasicAuth(userid,passcode), headers = {'X-CSRF-Token' : csrftoken } ,data = activate_payload)
    except Exception as e:
      f.write("Error while calling API to activate a version of an application\n")
      f.write("Error : %s\n" %(e))
      return

    if res.status_code == 200:
      f.write("Successfully activated version 1 of Test application : %s\n" %(html5testapp))
    else:
      f.write("Activating version 1 of test application: %s failed\n" % (html5testapp))
      f.write("Status Code : %s , Output : %s\n" % (res.status_code , res.text))
      return

# Start an application
    start_payload = "\"START\""
    START_URL = URL + html5testapp + "/action"
    try:
      res = c.post(START_URL, auth=HTTPBasicAuth(userid,passcode), headers = {'X-CSRF-Token' : csrftoken } ,data = start_payload)
    except Exception as e:
      f.write("Error while calling API to start an application\n")
      f.write("Error : %s\n" %(e))
      return

    if res.status_code == 200:
      f.write("Successfully started test application : %s\n" % (html5testapp))
    else:
      f.write("Start of test application, %s  failed\n" % (html5testapp))
      f.write("Status Code : %s , Output : %s\n" % (res.status_code , res.text))
      return
  return html5testapp

def getappurl(landscape, account,appname,f):

  landscape = landscape.lower()
  if landscape == "trial":
    BASEURL = "https://dispatcher.hanatrial.ondemand.com/hcproxy/b/api/accounts/"
  elif landscape == "eu1":
    BASEURL = "https://dispatcher.hana.ondemand.com/hcproxy/b/api/accounts/"
  else:
    BASEURL = "https://dispatcher." + landscape + ".hana.ondemand.com/hcproxy/b/api/accounts/"

  URL = BASEURL + account + "/applications/" + appname

# Get the URL of an application
  try:
    resp = requests.get(URL , auth = HTTPBasicAuth(userid, passcode))
  except Exception as e:
    f.write ("Error while calling API to get the details of app : %s\n" % (appname))
    f.write("Error : %s\n" %(e))
    return

  if resp.status_code == 200:
    json_data =  resp.json()
# Fetch application URL
    appurl = json_data['url']
    f.write("Name : %s , Status : %s , URL: %s \n" % (json_data['name'], json_data['status'], appurl))
    return appurl
  else:
    f.write("Error while fetching details of %s \n" % (appname))
    f.write("Status code : %s , Output : %s\n" % (resp.status_code, resp.text))
    return

    
if __name__ == "__main__":
  f = open('test.txt' ,'w+')
  designtime_scenario("TRIAL", f, 'i342592trial')
  f.close()

