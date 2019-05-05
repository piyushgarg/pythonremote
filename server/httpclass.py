import cgi
import datetime as dt
import http.server
import json
import re

import ar
from pythonremote import config_path

requestTracker = {}


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(b"<html><head><title>Pythonremote</title></head>")
        s.wfile.write(
            b"<p> This is index of python autoremote server. Nothing can be done here, go play some other place! </p>")
        s.wfile.write(b"</body></html>")
        print(vars(s))

    def do_POST(self):
        if None != re.search('/', self.path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'application/x-www-form-urlencoded' or ctype == 'application/json':
                length = int(self.headers.get('content-length'))
                body = self.rfile.read(length)
                jsondata = json.loads(body)


                # For some reason a http post req results in four requests
                # Extract one of them
                print("request")
                print(jsondata)  # print raw data
                if not isSameRequest(jsondata):
                    ar.request_received(config_path, jsondata)
                self.send_response(200, {})
                self.end_headers()
            else:
                data = {}
                self.send_response(200)
                self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()


def isSameRequest(received):
    actualSender = received['sender']
    duplicate = False
    if actualSender in requestTracker.keys():
        actualMessage = received['message']
        currentTimeStamp = dt.datetime.now()
        data = requestTracker[actualSender]
        if actualMessage in data.keys():
            previousTimeStamp = data[actualMessage]
            diff = currentTimeStamp - previousTimeStamp
            if diff.seconds < 3:
                print("D U P L I C A T E  R E Q U E S T   I G N O R I N G ................")
                duplicate = True

        data.update({received['message']: dt.datetime.now()})
    else:
        requestTracker.update({actualSender: {received['message']: dt.datetime.now()}})

    return duplicate
