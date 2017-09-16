###########################################################
#                Code by PvcJay@20170822                  #
#               It's only work on Python 2                #
#                      Version 0.1                        #
###########################################################

import os, socket, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

sda1Bool = False
sda2Bool = False
sda3Bool = False

# get local device free space
# use 'df -H' mount point

# /dev/sda3
dev_sda3 = os.statvfs('dev/XXX')
percent_sda3 = (dev_sda3.f_blocks - dev_sda3.f_bfree) * 100 / (dev_sda3.f_blocks - dev_sda3.f_bfree + dev_sda3.f_bavail) + 1

# # /dev/sda1
sda1 = os.statvfs('dev/XXX')
percent_sda1 = (percent_sda1.f_blocks - percent_sda1.f_bfree) * 100 / (percent_sda1.f_blocks -percent_sda1.f_bfree + percent_sda1.f_bavail) + 1

#/dev/sda2
sda2 = os.statvfs('dev/XXX')
percent_sda2 = (percent_sda2.f_blocks - percent_sda2.f_bfree) * 100 / (percent_sda2.f_blocks -percent_sda2.f_bfree + percent_sda2.f_bavail) + 1

# get host name transferm to name
hostIp = socket.gethostbyname(socket.gethostname())

def sendMail(msg):
    smtp_Server = 'smtp.gmail.com'
    
    gmailUser = 'yourEmail@gmail.com'
    gmailPassword = 'P@ssword'
    recipientlist = ['other1@domain.com','oter2@domain.com']


    mailMsg = MIMEMultipart()
    for recipient in recipientlist :
        mailMsg['From'] = gmailUser
        mailMsg['To'] = recipient
        mailMsg['Subject'] = "Subject of the email"
        mailMsg.attach(MIMEText(msg))

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmailUser, gmailPassword)
        mailServer.sendmail(gmailUser, recipient, mailMsg.as_string())
        mailServer.close()

    return

def checkDiskUsage(ip, percent_sda1 = 0, percent_sda2 = 0, percent_sda3 = 0):
    
    global sda1Bool, sda2Bool, sda3Bool, ipMsg_sda3

    # if usage are close 90% will send Email to notification

    if 90 <= percent_sda1 and percent_sda1 <= 99 : sda1Bool = True

    if 90 <= percent_sda2 and percent_sda2 <= 99 : sda2Bool = True
    
    if 10 <= percent_sda3 and percent_sda3 <= 20 : sda3Bool = True
    
    if (sda1Bool) :
        ipMsg_sda1 =  ip + " server's are full in sda1(/)."
        
    if (sda2Bool) :
        ipMsg_sda2 =  ip + " server's are full in sda2(/boot)."
        
    if (sda3Bool) :
        ipMsg_sda3 =  ip + " server's are full in sda3(/var/www/html)."

    sendMail(ipMsg_sda3)

    return

checkDiskUsage(hostIp, 0, 0, percent_sda3)
