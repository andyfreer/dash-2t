#!/usr/bin/env python

"""
Dash-2T
----

Dash second tier websockets and zeromq server

"""

import subprocess
import json

#importing the local one, with a patch
from websocket_server import WebsocketServer
from config import dashd_path, datadir

print dashd_path, datadir

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])

# Called for every client disconnecting
def client_left(client, server):
    print "disconnecting", client
    #print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    print("Client(%d) said: %s" % (client['id'], message))

    if(message.find("dapi_result") > 0 or message.find("dapi_message") > 0):
        print("Request broadcast %d" % client['id'])
        server.send_message_to_all(message)
    else:
        print dashd_path, datadir

        f = open("/Users/evan/Desktop/tmp", "wb")
        f.write(message)
        f.close()
        subprocess.call(dashd_path + " --datadir=" + datadir + " dapif /Users/evan/Desktop/tmp", shell=True)


PORT=5000
server = WebsocketServer(host="0.0.0.0", port=PORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()