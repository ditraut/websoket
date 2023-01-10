import json
import time
from websocket import WebSocketApp
import threading
import hashlib
import socket
import hmac
import hashlib
from datetime import datetime

class GateWebSocketApp_auth(WebSocketApp):
    IP_ADDRESS = "192.168.100.5"                      #BINDED IP
    PORT = 54893                                      #PORT

    def __init__(self, url, **kwargs):
        super(GateWebSocketApp_auth, self).__init__(url, **kwargs)

    def _request(self, channel, event=None, payload=None, auth_required=True):

        clientId = "s5MsEWHV"
        clientSecret = "TDhru3tRu9sjk1TZM0bfmkwB2HdyZ7NEBrZ68YmDGG0"
        timestamp = round(datetime.now().timestamp() * 1000)
        nonce = "abcd"
        data = ""
        signature = hmac.new(
            bytes(clientSecret, "latin-1"),
            msg=bytes('{}\n{}\n{}'.format(timestamp, nonce, data), "latin-1"),
            digestmod=hashlib.sha256
        ).hexdigest().lower()

        msg = {
            "jsonrpc": "2.0",
            "id": 8748,
            "method": "public/auth",
            "params": {
                "grant_type": "client_signature",
                "client_id": clientId,
                "timestamp": timestamp,
                "signature": signature,
                "nonce": nonce,
                "data": data
            }
        }

        msg = json.dumps(msg)
        print('request', msg)
        self.send(msg)

    def subscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "subscribe", payload, auth_required)

    def unsubscribe(self, channel, payload=None, auth_required=True):
        self._request(channel, "unsubscribe", payload, auth_required)


def on_message_auth(ws, message):
    print(message)


def on_open_auth(ws):
    print('Auth is Ok')
    ws.subscribe(False)


def auth():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((GateWebSocketApp_auth.IP_ADDRESS, GateWebSocketApp_auth.PORT))
    s.connect((GateWebSocketApp_auth.IP_ADDRESS, GateWebSocketApp_auth.PORT))
    print("Local ip is:",  s.getsockname()[0])

    app = GateWebSocketApp_auth("wss://www.deribit.com/ws/api/v2",
                           on_open=on_open_auth,
                           on_message=on_message_auth)
    app.run_forever(ping_interval=5)


if __name__ == "__main__":
    trd0 = threading.Thread(target=auth)
    trd0.start()
