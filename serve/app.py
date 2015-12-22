#!/usr/bin/env python

"""
Dash-2T
----

Dash second tier websockets and zeromq server

"""



import subprocess
import json
from websocket_server import WebsocketServer

dashd_path = "/Users/evan/Desktop/dash/src/dashd"
datadir = "/Users/evan/Desktop/.dash"

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print "disconnecting", client
    #print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))

    #subprocess.call([dashd_path, datadir, json.dumps(client)])


PORT=5000
server = WebsocketServer(PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()