import subprocess

from .color import color, yellow
from .load_computer import load_computer
from .message_send import message_send


# If message, check for saved response
def message_received(config_path, received, ardevice):
    print(color(yellow, "Received message. Checking for saved response."))
    message = received['message']  # "shell notify-send  -i  ~/Pictures/lock_grey_96x96.png  \"OTP is\""
    computer = load_computer(config_path)
    # option = message. split(" ")
    if message.startswith("shell"):
        cmd = message.replace("shell ", "")
        if cmd.find("\"") > 0:
            cmd = cmd.split("  ")
        else:
            cmd = cmd.split(" ")
        res = subprocess.check_output(cmd, universal_newlines=True)
        if res == "":
            return;
        response = "msg " + ardevice + " pythonremoteshellresp=:=" + res
        message_send(config_path, response)
    elif message.startswith("http"):
        cmd = "xdg-open \"" + message + "\""
        cmd = cmd.split(" ")
        print(cmd)
        subprocess.run(cmd)
        response = "msg " + ardevice + " urlopenresponse=:=opened"
        message_send(config_path, response)
