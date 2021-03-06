import urllib

import requests

from .color import color, green, red
from .load_computer import load_computer
from .load_device import load_device
from .message import Message


def message_send(config_path, indata):
    print("Trying to send message..")

    computer = load_computer(config_path)
    devlist = load_device(config_path)
    if indata.split()[1] in devlist:
        key = devlist[devlist.index(indata.split()[1]) + 1]

        msg_text = " ".join(indata.split()[2:])
        msg = Message(key, computer["id"], msg_text)  # GCM register device message

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post('https://autoremotejoaomgcd.appspot.com/sendmessage',
                          data=urllib.parse.urlencode(msg.__dict__), headers=headers)

        if r.text == "OK":  # If message is sent
            print(color(green, "Message successfully sent to device!"))
        else:
            print(color(red, "Couldn't send message. Aborting..."))
            exit(-1)
