# dependencies
import sys
import os
import json
import inquirer
import socketio
import time

# Setup Questions
connectiontypeask = [
    inquirer.List('contype',
        message="Control Console Connection Type:",
        choices=['localhost', 'remote']
    )
]

ipask = [
    inquirer.Text('ip', message="Control Console Connection IP:")
]

portask = [
    inquirer.Text('port', message="Control Console Connection Port:")
]


# Sub-modules

def CheckVersion():
    #Read file
    print("Checking Version...")
    config_file = open('config.json')
    keys = json.load(config_file)
    try:
        return keys["version"]
    except Exception as e:
        print("Failed to check version:")
        print(e)
        sys.exit(1)

def getState():
    try:
        config_file = open('config.json')
        config = json.load(config_file)
    except Exception as e:
        print("Failed to parse config.json")
        print(e)
        sys.exit(1)
    return config

# Main Functions

def setup():
    global bot_version
    bot_version = CheckVersion();
    # Conection SETUP
    # Questions
    print("Connection SETUP:")
    contype = inquirer.prompt(connectiontypeask)["contype"]
    if contype == "remote":
        ip = inquirer.prompt(ipask)["ip"]
        port = inquirer.prompt(portask)["port"]
    else:
        ip = "localhost"
        port = inquirer.prompt(portask)["port"]
    cadress = str(ip) + ":" + str(port)
    motd();
    main(cadress);

def motd():
    global bot_version
    print("===============================")
    print("MINIONS: OFFWHITE Bot")
    print(str(bot_version))
    print("===============================")

def main(ip):
    print("Waiting for control console with adress: "+ip+"...")
    sio = socketio.Client();

    @sio.event
    def connect():
        print("Connected to the control console!")
        print("Sending state...")
        state = getState();
        sio.emit('bot_states', state)

    @sio.event
    def disconnect():
        print("Disconnected from the control console!")
        print("Closing Socket...")
        sio.disconnect()
        main(ip);

    def init_connect():
        try:
            sio.connect('http://' + ip)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            if str(exc_obj) == "Connection refused by the server":
                #Wait 2 seconds and try again
                time.sleep(2)
                init_connect()
            else:
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error on SIO: ", exc_type, exc_obj, exc_tb.tb_lineno)

    init_connect();
    state = getState();
    ids = state["id"]

    @sio.on(ids)
    def on_message(data):
        print("Command Received: " + data)
        if data == "disconnect":
            print("Closing Socket...")
            sio.disconnect()
            sys.exit(1)
        elif "check_link" in data:
            print("Checking links...")
            checklinks = data.split()[1]
            print(checklinks)
        else:
            print("Invalid command")


if __name__ == '__main__':
    setup();
