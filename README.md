Dash2T
==============

Dash second tier websockets and zeromq server

Installation
------------

pip install requirements.txt
copy config.py.example config.py
python app.py


Notes
------------

On MAC OSX, reconnections yield the following error when they try to broadcast: 

Traceback (most recent call last):
  File "/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py", line 599, in process_request_thread
    self.finish_request(request, client_address)
  File "/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py", line 334, in finish_request
    self.RequestHandlerClass(request, client_address, self)
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 136, in __init__
    StreamRequestHandler.__init__(self, socket, addr, server)
  File "/usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/2.7/lib/python2.7/SocketServer.py", line 655, in __init__
    self.handle()
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 149, in handle
    self.read_next_message()
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 194, in read_next_message
    self.server._message_received_(self, decoded)
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 100, in _message_received_
    self.message_received(self.handler_to_client(handler), self, msg)
  File "app.py", line 36, in message_received
    server.send_message_to_all(message)
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 73, in send_message_to_all
    self._multicast_(msg)
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 123, in _multicast_
    self._unicast_(client, msg)
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 119, in _unicast_
    to_client['handler'].send_message(msg)
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 197, in send_message
    self.send_text(message)
  File "/usr/local/lib/python2.7/site-packages/websocket_server/websocket_server.py", line 243, in send_text
    self.request.send(header + payload)
error: [Errno 32] Broken pipe


To fix this error find websocket_server.py

def _unicast_(self, to_client, msg):
    try:
        to_client['handler'].send_message(msg)
    except:
        pass
```