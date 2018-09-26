# -*- coding: utf-8 -*-
#!/usr/bin/python3


BASE_URL="https://www.site24x7.com/api/"
header={'Authorization':'Zoho-authtoken 1069b6411310185ce5aa553337252ce8'}

#SMTP Params
smtp_host = "mail.sap.corp"
smtp_port = 587
sender = "noreply+scp-ce-alerts@sap.com"
recipients = ['DL_567132A95F99B77D07000002@exchange.sap.corp']
username = 'scp-ce-alerts'
password = 'abc@1234'

#IAS US Params
IAS_US_GID = '86388000009889424'

#Core Monitors
IAS_US_C = ['86388000009941161', '86388000002508135']

#Primary DC - Converged Cloud (Sterling) 
IAS_US_PRM = ['86388000014061031']

# Secondary DC ( Toronto)
IAS_US_SEC = ['86388000014593003']

#IAS US commands
IAS_US_CMDS = ['curl -D - https://us1.accounts.ondemand.com/health', 'curl -D - https://na-us-1.accounts.ondemand.com/health' , 'curl -D - https://na-ca-1.accounts.ondemand.com/health','ping -c 3 us1.accounts.ondemand.com','nslookup us1.accounts.ondemand.com','traceroute us1.accounts.ondemand.com -p 443']

#IAS EU Params

#SAP CP IAS - EU
IAS_EU_GID = '86388000009889422'

#Core Monitors
IAS_EU_C = ['86388000002508085','86388000009699997','86388000012796401','86388000009726005','86388000013571225']

# Secondary DC – Monsoon 2 Rot
IAS_EU_SEC = ['86388000009699293','86388000009699285']

# Primary DC – Converged Cloud Rot
IAS_EU_PRM = ['86388000009726259','86388000009047917']

#Backup DC – Converged Cloud Amsterdam
IAS_EU_BAK = ['86388000009726269','86388000009047925']

#IAS Commands
IAS_EU_CMDS = ['curl -D - https://accounts.sap.com/health','curl -D - https://eu1.accounts.ondemand.com/health','ping -c 3 accounts.sap.com' , 'nslookup accounts.sap.com', 'traceroute accounts.sap.com -p 443', 'nslookup https://eu1.accounts.ondemand.com', 'ping -c 3 eu1.accounts.ondemand.com', 'traceroute eu1.accounts.ondemand.com -p 443']

# Helium Dispatcher Parameters
HEL_GID = '86388000005536007'
subaccount = 'i342592trial'
html5testapp = 'html5testapp'
html5testrepo = subaccount + '/testapp'

#Lifecycle Management parameters
HCP_LM_GID = '86388000003121001'
PATTERN = "C Lifecycle Management"

# Username and password for API Authentication
userid =
passcode = 

# Proxy details
http_proxy  = "http://147.204.6.136:8080"
https_proxy = "https://147.204.6.136:8080"
ftp_proxy   = "ftp://147.204.6.136:8080"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }
