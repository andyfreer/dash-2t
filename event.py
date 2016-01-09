#!/usr/bin/env python

"""
Dash-2T
----

Dash Event

"""

import argparse
from websocket import create_connection

parser = argparse.ArgumentParser(description='dash event script')
parser.add_argument('--event')
args = parser.parse_args()

if args.event:
    # with open(args.event, 'r') as myfile:
    #     data=myfile.read().replace('\n', '')

    ws = create_connection("ws://localhost:5000")
    print args.event
    ws.send(args.event)
    result =  ws.recv()
    print "Received '%s'" % result
    ws.close()