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
from config import dashd_path, datadir, eventfile
from email_sender import SendValidationEmail

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

    """
    look for object like this one:
    {"object":"dapi_result",
        "data":{"id":"1111","command":"invite_user","error_id":0,"error_message":"",
            "data":{"status":1,"username":"cryptofish82","name":"Evan Duffield","email":"cryptofish82@gmail.com","challenge_code":"486895"}
        }
    }
    """    
    try:
        obj = json.loads(message)
    except:
        print "invalid json", message
        return 

    if(obj["object"] == "dapi_result" and obj["data"]["command"] == "invite_user" and obj["data"]["error_id"] == 0):
        SendValidationEmail("masternode@dashevolution.com", obj["data"]["data"]["email"], obj["data"]["data"]["name"], "dashevolution_com", obj["data"]["data"]["username"], obj["data"]["data"]["challenge_code"])

    if(message.find("dapi_result") > 0 or message.find("dapi_message") > 0):
        print("Request broadcast %d" % client['id'])
        server.send_message_to_all(message)
    else:
        print dashd_path, datadir

        f = open(eventfile, "wb")
        f.write(message)
        f.close()
        subprocess.call(dashd_path + " --datadir=" + datadir + " dapif " + eventfile, shell=True)


import fasteners
import threading
a_lock = fasteners.InterProcessLock('/tmp/t2-websockets')

def test_cpu():
    # giant hack incoming for some high cpu bug:
    import psutil
    import sys
    print psutil.cpu_percent() 
    if psutil.cpu_percent() > 50:
        print "cpu too high, exiting"
        sys.exit()

gotten = a_lock.acquire(blocking=False)
try:
    if gotten:
        print('I have the lock')

        print "start test cpu thread"
        #kill the process if the cpu is high
        threading.Timer(10, test_cpu).start()

        PORT=5000
        server = WebsocketServer(host="0.0.0.0", port=PORT)
        server.set_fn_new_client(new_client)
        server.set_fn_client_left(client_left)
        server.set_fn_message_received(message_received)
        server.run_forever()
        
    else:
        print "already running"
        exit()
finally:
    if gotten:
        print "release"
        a_lock.release()

