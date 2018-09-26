# -*- coding: utf-8 -*-
#!/usr/bin/python3


import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import smtplib
import logging
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
from settings import smtp_host, smtp_port, sender, recipients, username, password

def send_mail(region,subject, down_list,filename, primary_status,secondary_status,backup_status=None):
  if region == 'EU':
    procedure = "Failover process will happen from Converged Cloud (Rot) --> Monsoon 2 (Rot) --> Converged Cloud (Amsterdam)"
  if region == 'US':
    procedure = "Failover process will happen from Converged Cloud (Sterling) --> Converged Cloud (Toronto)"
  message = MIMEMultipart()
  message['From'] = sender
  message['To'] = COMMASPACE.join(recipients)
  message['Date'] = formatdate(localtime=True)
  message['Subject'] = subject
  # Message Body
  html= """\

<html>

<head></head>
<h4><b><u><center>IAS """+region+""" Region Status: </center></h4></u></b>
<ol>
  <li> <font size="3" color="red"> Down Monitor(s) : """ + str(down_list) + """ </font> </li>
  <li>Primary DC Status : """+str(primary_status)+"""</li>
  <li>Secondary DC Status : """+str(secondary_status)+"""</li>
  <li>Backup DC Status : """+str(backup_status)+ """</li>
  </br>
  <li><b><u>Next Steps for CE: </u></b></li>
  <ul>
    <li> Analyze the results in attached document. </li> 
    <li> If Primary DC monitor is down , it should failover to the secondary ones. """ + procedure + """ </li>
    <li> Open a Bridge call using the attached Bridge_Call_Template.</li>
    <li> Include <a href = "https://wiki.wdf.sap.corp/wiki/display/CloudEng/Developer+and+Manager+OnDuty+Contacts+and+Scheduling"> Neo MoD.</a> </li>
    <li> Call IAS Hotline: +359-2-9157-300 </li>
    <li> Send <a href="https://manage.statuspage.io/pages/2v74h7grp536"> customer annoucement </a>. </li>
    <li> Check the <a href = "https://status-iaas.itc.sap.com/">Cloud Infrastructure Statuspage</a>  for any ongoing outage. </li>
    <li> In case of N/W issue with primary DC : Create an incident to Network Team  in the component “NW_CLOUD_CC” and provide the details(source and destination) attached in the mail.</li>
    <li> Call CIS MOD  +49 6227766550, select option #1 and ask him to engage Converged Cloud  N/W colleagues to check the issue with primary DC</li>
<br>
<br>

</html>
"""

  body = MIMEText(html, 'html')
  message.attach(body)
# For IAS
  files = ['Bridge_Call_Template_IAS_Cloud_Engineering.msg']
  files.append(filename)
  # Text File Attachement
  for f in files:
    with open(f,'rb') as fil:
      part = MIMEApplication( fil.read() , Name = basename(f) )
      part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
      message.attach(part)

  try:    
    logging.info("Sending email...")
    server=smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(sender,recipients, message.as_string())
    logging.info("Email sent successfully")
  except smtplib.SMTPException as e:
    logging.error("Error: Unable to send email")
    logging.error(e)
  finally:
    server.quit()
