const fs = require('fs');
const chalk = require('chalk');

//Essentials for notifications
var notifications = {"ready": "Ready, waiting for console"}
exports.evalState = function(state) {
    if (notifications.hasOwnProperty(state)) {
      return notifications[state]
    } else {
      return state
    }
}


exports.list = function(bots) {
  console.log(chalk.grey("Registered BOTS:"))
  /*
  ID: BOT_SUPREME0 | State: CONNECTED - UNSET
  */
  Object.keys(bots).forEach(function(key) {
    if (bots[key]["connection"] == true) {
      console.log(chalk.grey("ID: " + key + " | State: ") + chalk.green("CONNECTED") + " - " + bots[key]["state"].toUpperCase() + chalk.grey(" | Links: " + bots[key]["link"]))
    } else {
      console.log(chalk.grey("ID: " + key + " | State: ") + chalk.red("DISCONNECTED") + " - " + bots[key]["state"].toUpperCase() + chalk.grey(" | Links: " + bots[key]["link"]))
    }
  });
}

exports.check_disconnect = function(bots, dataarg) {
  console.log("[SERVER]: Disconnecting "+dataarg+"...");
  try {
    if (bots.hasOwnProperty(dataarg)) {
      if (!bots[dataarg]["connection"]) {
        console.log("[SERVER]: " + dataarg + " is not connected")
        return false;
      } else {
        bots[dataarg]["connection"] = false;
        return true;
      }
    } else {
      console.log("[SERVER]: " + dataarg + " is not registered")
    }
  } catch(e) {
    console.error("[SERVER]: Unable to disconnect " + dataarg)
    console.error(chalk.red(e))
    return false;
  }
}

exports.set_link = function(bots, target, link) {
  console.log("[SERVER]: Setting links for "+target+"...");
  try {
    if (bots.hasOwnProperty(target)) {
      bots[target]["link"] = link
      console.log("[SERVER]: " + chalk.green("Links set ("+target+")"))
      return true;
    } else {
      console.log("[SERVER]: " + target + " is not registered")
      return false;
    }
  } catch(e) {
    console.error("[SERVER]: Unable to set link on " + target)
    console.error(chalk.red(e))
    return false;
  }
}
