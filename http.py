from flask import Flask, request, redirect
from websocket import create_connection
import json
import re
from random import randint

app = Flask(__name__)

"""

    Example URL:

    http://localhost:9000/api/v1/payment-request?username_merchant=aoeu&username_client=evan&amount=123000&address=XtvW7UMfabhYShm7ZHaVVdiwg2AHX8phST&description=test%20item&callback_url=https%3A%2F%2Fwww.google.com%2F%23q%3D%tx%
"""

@app.route("/api/v1/payment-request", methods=['POST', 'GET'])
def payment_request():
    username_merchant = None
    username_client = None
    amount = None
    address = None
    description = None
    callback_url = None
    signature = None

    result = { 
        "object" : "dapi_result",
        "data" : {
            "command" : "send_message",
            "sub_command" : "payment-request",
            "error_id" : 0,
            "error_message" : ""
        }
    }

    if request.method == 'POST':
        pass
        #username = request.form['username']
    elif request.method == 'GET':
        if 'username_merchant' in request.args:
            username_merchant = request.args.get('username_merchant')
        if 'username_client' in request.args:
            username_client = request.args.get('username_client')
        if 'amount' in request.args:
            amount = request.args.get('amount')
        if 'address' in request.args:
            address = request.args.get('address')
        if 'description' in request.args:
            description = request.args.get('description')
        # if 'callback_url' in request.args:
        #     callback_url = request.args.get('callback_url')
        if 'signature' in request.args:
            signature = request.args.get('signature')
        
        """
        username_merchant: The merchant`s username on the network
        username_client: The client`s username on the network 
        requested_amount: The cost of the item or service in satoshis
        description: Description of item, such as "6x White Socks"
        callback_url: The URL the network will callback when a status is known
        signature: merchant signature of all fields
        """
        
        result["data"]["from_uid"] = username_merchant
        result["data"]["to_uid"] = username_client
        result["data"]["signature"] = signature
        result["data"]["payload"] = json.dumps({'amount' : amount, 'address' : address, 'description' : description})

    """
        Validate data before sending it to the user
    """


    if not username_merchant:
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Missing required parameter: username_merchant";
    if not username_client:
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Missing required parameter: username_client";
    if not amount:
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Missing required parameter: amount";
    if not address:
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Missing required parameter: address";
    if not description:
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Missing required parameter: description";
    if not callback_url:
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Missing required parameter: callback_url";
    # if not signature:
    #     result["data"]["error_id"] = 1010;
    #     result["data"]["error_message"] = "Missing required parameter: signature";
        

    m = re.search('[a-zA-Z0-9]+', address)
    if not m:
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Invalid Dash Address";

    m = re.search('^[0-9]+$', amount)
    if not m or amount[0] == ".":
        result["data"]["error_id"] = 1010;
        result["data"]["error_message"] = "Invalid amount";


    if result["data"]["error_id"] == 0:
        payment_id = randint(1,1000000)
        obj = { 
            "object" : "dapi_command",
            "data" : {
                "payment_id" : payment_id,
                "command" : "send_message",
                "sub_command" : "payment-request",
                "from_uid" : username_merchant,
                "to_uid" : username_client, 
                "signature" : signature,
                "payload" : json.dumps({'amount' : amount, 'address' : address, 'description' : description})
            }
        }

        ws = create_connection("ws://localhost:5000")
        ws.send(json.dumps(obj))

        waiting = True
        while waiting:
            result2 =  json.loads(ws.recv())

            print "New result '%s'" % result2

            if result2['object'] == "dapi_message" and result2["data"]["sub_command"] == "payment-request-result":
                waiting = False

                print "Found Match '%s'" % result

                obj2 = json.loads(result2["data"]["payload"]);
                if obj2["status"] == "success":
                    result["data"]["error_id"] = 0;
                    result["data"]["error_message"] = ""
                    # callback_url = callback_url.replace("%status%", obj2["status"])
                    # callback_url = callback_url.replace("%tx%", obj2["tx"])
                    # return redirect(callback_url, 302)
                if obj2["status"] == "failure":
                    result["data"]["error_id"] = 1015;
                    result["data"]["error_message"] = "User failed to send transaction"

                    # callback_url = callback_url.replace("%status%", "User%20failed%20to%20send%20transaction.")
                    # callback_url = callback_url.replace("%tx%", "")
                    # return redirect(callback_url, 302)

        ws.close()

    #print result

    # callback_url = callback_url.replace("%status%", "failure")
    # callback_url = callback_url.replace("%tx%", "")
    # return redirect(callback_url, 301)

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return json.dumps(result)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=9000)