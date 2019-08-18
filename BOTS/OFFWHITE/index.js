const fs = require('fs')
const chalk = require('chalk');
const inquirer = require('inquirer');
const core = require('./botcore.js')
const spawn = require("child_process").spawn;
var pythonProcess;
var bot_version;
var socket;
var cadress;
var cnfparser;
//Parse Package details
console.log("Checking Version...")
const fileContents = fs.readFileSync('./package.json', 'utf8')
try {
  const data = JSON.parse(fileContents)
  bot_version = data["version"];
} catch(err) {
  console.error("Failed to check version")
  console.error(err)
  process.exit(1)
}

console.log("Connection SETUP:")
var connectiontypeask = [
{
    type: 'list',
    name: 'contype',
    message: chalk.white("Control Console Connection Type:"),
    choices: ['localhost', 'remote'],
    filter: function (val) {
        return val.toLowerCase();
    }
}];
var ipask = [{
    type: 'input',
    name: 'ip',
    message: chalk.white("Control Console Connection IP:"),
}];
var portask = [{
    type: 'input',
    name: 'port',
    message: chalk.white("Control Console Connection Port:"),
}];
var ip;
var port;

inquirer.prompt(connectiontypeask)
.then(answer => {
    if(answer["contype"] == "remote") {
      inquirer.prompt(ipask)
      .then(answer => {
          ip = answer["ip"]
          inquirer.prompt(portask)
          .then(answer => {
              port = answer["port"]
              initsetup();
          });
      });
    } else {
      inquirer.prompt(portask)
      .then(answer => {
          port = answer["port"]
          initsetup();
      });
    }
});

function initsetup() {
  //Create Connection Adress
  if (ip) { //Remote
    cadress = ip + ":" + port
  } else {
    cadress = "localhost:" + port
  }
  motd();
  cnfparser = setInterval(cnf_parser, 1000)
  main(cadress);
}

function cnf_parser() {
  state = core.getState();
  if (state["state"] == "shutdown") {
    console.error("BOT SHUTDOWN - Check Logs on PY_Scripts")
    if (socket || socket.connected) {
      socket.disconnect();
    }
    process.exit(1)
  }
}

function shutdown_bot() {
  console.log("Sending Bot Shutdown...")
  sdcnf = {'state': 'shutdown'}
  tmpcmd = spawn('python',["PY_Scripts/cnf_modifier.py", '-c "' + JSON.stringify(sdcnf) + '"'])
  tmpcmd.stdout.on('data', (chunk) => {
    data = chunk.toString('utf8');
    console.log(data)
  });
}

function motd() {
  console.log("===============================")
  console.log("MINIONS: OFFWHITE Bot")
  console.log(bot_version)
  console.log("===============================")
}

function main(ip) {
  //Check for updates with version
  console.log("Waiting for control console with IP "+ip+"...")
  socket = require('socket.io-client')('http://' + ip);
  socket.on('connect', function(){
    console.log(chalk.green("Connected to the control console!"))
    console.log("Sending state...")
    state = core.getState();
    socket.emit('bot_states', state)
  });
  //Channel of BOT
  state = core.getState();
  ids = state["id"];
  socket.on(ids, function(data){
    console.log("Command Received: " + data)
    if (data == "disconnect") {
      console.log("Closing Socket...")
      socket.disconnect();
      clearInterval(cnfparser);
      shutdown_bot();
      console.log("Shutting Down...")
      //process.exit();
    }
    if (data.includes("check_link")) {
      //Grab Link and send to checker
      dataarg = data.split(/\s+/)[1];
      console.log("Checking Link: " + dataarg)
      core.getMainLink(dataarg, function(arg){
        console.log(arg)
      });
    }
  });

  socket.on('disconnect', function(){
    console.log("Disconnected from the control console!")
    console.log("Closing Socket...")
    socket.disconnect();
    main(ip);
  });

}
