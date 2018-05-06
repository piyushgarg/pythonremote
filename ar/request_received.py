from .color import color, red, yellow
from .message_received import message_received
from .notification_received import notification_received
from .register_device import register_newdevice, register_sendtodevice


# Function for processing a request
def request_received(config_path, received):
    f = open(config_path + "autoremotedevices.txt", "r")
    devlist = f.read().split("\n")

    # Check if known and respond
    if received["sender"] in devlist:
        print(color(yellow, "You just received something from " + devlist[devlist.index(received["sender"]) - 1] + "!"))
        if received["communication_base_params"]["type"] == "Notification":
            notification_received(received)
        elif received["communication_base_params"]["type"] == "Message":
            message_received(config_path, received, devlist[devlist.index(received["sender"]) - 1])
        elif received["communication_base_params"]["type"] == "RequestGetRegistration":
            register_sendtodevice(config_path, received["sender"])
        elif received["communication_base_params"]["type"] == "RequestSendRegistration":
            if received["id"] not in devlist:
                register_sendtodevice(config_path, received["sender"])
        elif received["communication_base_params"]["type"] == "RequestSendRegistrations":
            for device in received["devices"]:
                id = device["id"]
                name = device["name"]
                print(name)
                if id not in devlist:
                    register_newdevice(config_path, "", name, id, "no")


    else:
        print(color(red, "You just received something from unknown device!!"))
        print(color(red, "Device key: " + received["sender"]))

    f.close()
    # print(received)
