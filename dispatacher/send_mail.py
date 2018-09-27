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

def send_mail(region,subject,result,filename):
  message = MIMEMultipart()
  message['From'] = sender
  message['To'] = COMMASPACE.join(recipients)
  message['Date'] = formatdate(localtime=True)
  message['Subject'] = subject

  # Message Body
  html= """\

<html>

<head></head>
<h4><b><u><center> HTML5 Application Runtime status in """ + region + """ Landscape  </center></h4></u></b>
<ol>
  <li> <font size="3" color="red">Analysis Result : """ + str(result) + """</font></li>
  <li><b><u>Next Steps for CE: </u></b></li>
  <ul>
    <li> Analyze the results in the attached document & check the impact. </li> 
    <li> If dispatcher processes are in critical state, give focus on <b>MaxTenantRequests</b> & <b>BusyThreads</b> ( as these are the major & critical metrics which can potentially impact). </li>
    <li> Check <a href = "http://mo-8b3baf8ff.mo.sap.corp:3000/dashboard/db/html5runtimeandsupportportaldispatcher" > Grafana Dashboard </a>(username:anzeiger, password: display) and check the metrics in affected landscape (<b>SupportPortal </b>is one of the major stakeholders of Helium Application).</li>
    <li> Decide(based on the results) & Open Bridge call using the attached <b>Dispatcher_Bridge_Call_Template</b>.</li>
    <li> Contact <a href = "https://wiki.wdf.sap.corp/wiki/display/hcproxy/DoD+Schedule"> DoD.</a> </li>
    <li> Include <a href = "https://wiki.wdf.sap.corp/wiki/display/CloudEng/Developer+and+Manager+OnDuty+Contacts+and+Scheduling"> Neo MoD.</a> </li>
    <li> Check <a href= "https://jtrack.wdf.sap.corp/browse/SERVICE-15" > SERVICE-15 </a> for further information. </li>
    <li> Send <a href="https://manage.statuspage.io/pages/2v74h7grp536"> Customer Annoucement </a>. </li>
  </ul>
</ol>
<br>

</html>
"""

  body = MIMEText(html, 'html')
  message.attach(body)
# For Dispatcher
  files = ['Dispatcher_Bridge_Call_Template_Cloud_Engineering.msg']
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
