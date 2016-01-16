#!/usr/bin/python

import smtplib

def SendValidationEmail(sender, receiver, name, from_uid, to_uid, code):
    receivers = [receiver]

    message = """From: Dash Network <masternode@dashevolution.com>
To: """+to_uid+""" <"""+receiver+""">
Subject: Please confirm your signup to Dash Evolution


Hello """ + to_uid + """,

Welcome to Dash Evolution!

Please confirm your signup using this link:

http://www.dashevolution.com/#/signup/confirm/"""+from_uid+"""/"""+to_uid+"""/"""+code+"""

To learn more about Dash Evolution please check out our documentation and source here:

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