#!/usr/bin/python

import smtplib

def SendValidationEmail(sender, receiver, name, from_uid, to_uid, code):
    receivers = [receiver]

    message = """From: Dash Network <masternode@dashevolution.com>
To: """+to_uid+""" <"""+receiver+""">
Subject: Please validate your email for DashEvolution


Hello """ + to_uid + """,

It looks like you just registered an account for DashEvolution. To validate your email, please click the following link. 
Afterward you should be able to login to your wallet and start using it.

http://www.dashevolution.com/#/signup/confirm/"""+from_uid+"""/"""+to_uid+"""/"""+code+"""

For more information about using dash evolution, watch the video here:

http://www.dash.org/evolution

Thank you,

The Dash Network
    """

    print message

    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receivers, message)
       print "Successfully sent email"
    except:
       print "Error: unable to send email"