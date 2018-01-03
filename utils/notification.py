#!/usr/bin/env python
import smtplib

def sendmail(title, content):
    From = 'notification@securityapp.store' 
    #From = 'root@mail.securityapp.store' 
    To = "liuwenmao@126.com" 
    To = "marvelliu@gmail.com" 
    Subject = '[New notification] %s'%title
    Content = content 
    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (From, To, Subject, Content)
#""" % (From, ", ".join(To), Subject, Content)
    
    s = smtplib.SMTP_SSL('mail.securityapp.store')
    s.sendmail(From, [To], message)
    s.quit()
    
