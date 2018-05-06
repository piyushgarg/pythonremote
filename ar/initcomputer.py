import json
import os

from .color import color, green, red, yellow
from .getip import get_lanip, get_pubip
from .keygen import keygen
from .load_computer import load_computer
from .register_device import register_updatedevice


# Function for creating server data
def initcomputer(config_path):
    if os.path.isfile(config_path + "autoremote.json"):
        print(color(green, "Autoremote config json file exists. Continuing server startup.."))

        computer = load_computer(config_path)

        lanip = get_lanip()
        pubip = get_pubip()
        change = "false"

        if computer["localip"] == lanip:
            print(color(green, "LAN IP is up to date.."))
        else:
            print(color(yellow, "LAN IP is being updpated"))
            computer["localip"] = lanip
            change = "true"

        if computer["publicip"] == pubip:
            print(color(green, "Public IP is up to date.."))
        else:
            print(color(yellow, "Public IP is being updated"))
            computer["publicip"] = pubip
            change = "true"

        # Write json to file
        if change == "true":
            try:
                fd = open(config_path + 'autoremote.json', 'w+')
                fd.write(json.dumps(computer, indent=4))
                fd.close()
            except:
                print(color(red, "ERROR writing autoremote.json..."))
                exit(-1)
            register_updatedevice(config_path)

    else:
        print(color(yellow, "Autoremote config json file doesnt exist."))
        answr = input(color(yellow, "Do you want to configure this device? [y/n] "))
        if answr in ['y', 'yes', 'Y', 'YES']:
            computer = json.loads(
                '{"type":"eventghost","port":"1818","haswifi":"True","ttl":"0","collapsekey":"0","additional":{"type":"EventGhost","canreceivefiles":"True","canReceiveNotifications":"True"},"communicattestion_base_params":{"type":"RequestSendRegistration"}}')
            # Ask for needed parameters
            computer["id"] = "EventGhost"  # input("Id: ")
            computer["name"] = "EventGhost"  # input("Name: ")
            computer["localip"] = get_lanip()
            computer["publicip"] = get_pubip()
            computer["sender"] = "EventGhost"  # input("Sender: ")
            computer["key"] = keygen(30)  # input("key: ")

            computer["communication_base_params"]["sender"] = computer["sender"]

            icon = "linux"  # input("Icon(mac/linux/windows or URL to icon): ")
            if icon == "mac":
                icon = "http://icons.iconarchive.com/icons/osullivanluke/orb-os-x/512/OSX-icon.png"
            elif icon == "linux":
                icon = "http://icons.iconarchive.com/icons/tatice/operating-systems/256/Linux-icon.png"
            elif icon == "windows":
                icon = "http://icons.iconarchive.com/icons/benjigarner/softdimension/256/Windows-icon.png"

            computer["additional"]["iconUrl"] = icon

            # Write json to file
            try:
                fd = open(config_path + 'autoremote.json', 'w+')
                fd.write(json.dumps(computer, indent=4))
                fd.close()
            except:
                print(color(red, "ERROR writing autoremote.json..."))
                exit(-1)
            register_updatedevice(config_path)

    return computer
