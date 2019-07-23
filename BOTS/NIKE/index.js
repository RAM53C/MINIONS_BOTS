const fs = require('fs')
const chalk = require('chalk');
const inquirer = require('inquirer');
const core = require('./botcore.js')
var bot_version;
var socket;
var cadress;
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
  main(cadress);
}


function motd() {
  console.log("===============================")
  console.log("MINIONS: Nike Bot")
  console.log(bot_version)
  console.log("===============================")
}

function main(ip) {
  //Check for updates with version
  console.log("Waiting control console with IP "+ip+"...")
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
      console.log("Shutting Down...")
      process.exit();
    }
    if (data.includes("check_link")) {
      //Grab Link and send to checker
      dataarg = data.split(/\s+/)[1];
      console.log("Checking Link: " + dataarg)

    }
  });

  socket.on('disconnect', function(){
    console.log("Disconnected from the control console!")
    console.log("Closing Socket...")
    socket.disconnect();
    main(ip);
  });

}
