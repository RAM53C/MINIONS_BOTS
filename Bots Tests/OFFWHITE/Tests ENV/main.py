# dependencies
import sys
import os
import json
import inquirer
import socketio
import time
import threading
import subprocess

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

#BOT Parser
def cnf_update(): #Refresh time: 2 seconds
    global sio
    print("Loading Bot Parser...")
    cp = threading.currentThread()
    while getattr(cp, "do_run", True):
        state = getState();
        sio.emit('bot_states', state)
        time.sleep(3)

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
    os.system("python cnf_modifier.py -c \"{'state':'unset'}\"")
    initialize_bot();
    main(cadress);

def motd():
    global bot_version
    print("===============================")
    print("MINIONS: OFFWHITE Bot")
    print(str(bot_version))
    print("===============================")

def initialize_bot():
    print("Initializing Bot...")
    os.system("xterm -e \"python3 bot_core.py\" &")

def stop_bot():
    print("Stopping Bot...")
    os.system("python cnf_modifier.py -c \"{'state':'shutdown'}\"")

def main(ip):
    global sio
    print("Waiting for control console with adress: "+ip+"...")
    sio = socketio.Client();

    @sio.event
    def connect():
        global cpw
        print("Connected to the control console!")
        print("Initializing state update...")
        threads = []
        cpw = threading.Thread(target=cnf_update);
        cpw.start();

    @sio.event
    def disconnect():
        global cpw
        print("Disconnected from the control console!")
        cpw.do_run = False
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
            global cpw
            cpw.do_run = False
            print("Closing Socket...")
            sio.disconnect()
            stop_bot()
            sys.exit(1)
        elif "check_link" in data:
            print("Checking links...")
            checklinks = data.split()[1]
            os.system("python cnf_modifier.py -c \"{'product_url':"+checklinks+", 'state':'check'}\"")
        elif data == "rlsolve":
            print("Removing rejected links...")
            os.system("python cnf_modifier.py -c \"{'rejected_links':[], 'state':'check'}\"")
        elif data == "start":
            print("Starting BOT...")
            os.system("python cnf_modifier.py -c \"{'state':'start'}\"")
        elif data == "stop":
            print("Stopping BOT...")
            os.system("python cnf_modifier.py -c \"{'state':'stop'}\"")
        else:
            print("Invalid command")


if __name__ == '__main__':
    setup();
