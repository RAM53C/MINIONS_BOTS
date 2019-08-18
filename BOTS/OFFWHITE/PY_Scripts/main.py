# dependencies
import sys
import os
import json
import inquirer
import socketio

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
    sio = socketio.AsyncClient()
    await sio.connect('http://' + ip)

    @sio.event
    async def connect():
        print("Connected to the control console!")
        print("Sending state...")
        state = getState();
        await sio.emit('bot_states', state)

    state = getState();
    ids = state["id"]

    @sio.on(ids)
    async def on_message(data):
        print("Command Received: " + data)
        if data == "disconnect":
            print("Closing Socket...")
            await sio.disconnect()
            sys.exit(1)
        elif "check_link" in data:
            print("Checking link...")
        else:
            print("Invalid command")

    @sio.event
    async def disconnect():
        print("Disconnected from the control console!")
        print("Closing Socket...")
        await sio.disconnect()
        main(ip);


if __name__ == '__main__':
    setup();
