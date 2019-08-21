const fs = require('fs');
const chalk = require('chalk');
const warning = chalk.keyword('orange');

//Essentials for notifications
var notifications = {"ready": "chalk.green('Ready, waiting for console')", "check": "Checking Links..."}
exports.evalState = function(state, rl) {
    if (Array.isArray(rl) && rl.length) {
      console.log(warning("[SERVER][WARNING]: There are rejected links, please run 'list rl' to see them"))
    }
    if (notifications.hasOwnProperty(state)) {
      return eval(notifications[state])
    } else {
      return state
    }
}

exports.listrl = function(bots) {
  console.log(chalk.grey("Rejected Links:"))
  Object.keys(bots).forEach(function(key) {
    rlss = bots[key]["rejected_links"]
    if (Array.isArray(rlss) && rlss.length) {
      rls = bots[key]["rejected_links"]
      console.log(chalk.grey("ID: " + key))
      console.log(chalk.grey("Rejected links: "))
      rls.forEach(function(element) {
        console.log(chalk.grey(element));
      });
      console.log(chalk.grey("=========================="))
    } else {
      console.log(chalk.grey("ID: " + key))
      console.log(chalk.grey("Rejected links: None"))
    }
  });
  console.log("To solve this issue you can run 'rl solve -all' or reset the links using 'set link' feature")
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
      console.log("[SERVER]: Links set on " + target)
      return true;
    } else {
      console.log("[SERVER]: " + target + " is not registered")
      return false;
    }
  } catch(e) {
    console.error("[SERVER]: Unable to set links on " + target)
    console.error(chalk.red(e))
    return false;
  }
}

exports.botsrl = function(bots) {
  console.log("[SERVER]: Removing rejected links...")
  rlbots = []
  Object.keys(bots).forEach(function(key) {
    rlss = bots[key]["rejected_links"]
    if (Array.isArray(rlss) && rlss.length) {
      rlbots.push(key)
    }
  });
  return rlbots;
}

exports.check_start = function(bots, dataarg) {
  console.log("[SERVER]: Starting "+dataarg+"...");
  try {
    if (bots.hasOwnProperty(dataarg)) {
      if (!bots[dataarg]["state"] == "ready") {
        console.log("[SERVER]: Unable to start " + dataarg + ": Current state is <"+bots[dataarg]["state"]+"> and not <ready>")
        return false;
      } else {
        return true;
      }
    } else {
      console.log("[SERVER]: " + dataarg + " is not registered")
    }
  } catch(e) {
    console.error("[SERVER]: Unable to start " + dataarg)
    console.error(chalk.red(e))
    return false;
  }
}


exports.check_stop = function(bots, dataarg) {
  console.log("[SERVER]: Stopping "+dataarg+"...");
  try {
    if (bots.hasOwnProperty(dataarg)) {
      if (!bots[dataarg]["state"] == "working") {
        console.log("[SERVER]: Unable to stop " + dataarg + ": Current state is <"+bots[dataarg]["state"]+"> and not <ready>")
        return false;
      } else {
        return true;
      }
    } else {
      console.log("[SERVER]: " + dataarg + " is not registered")
    }
  } catch(e) {
    console.error("[SERVER]: Unable to stop" + dataarg)
    console.error(chalk.red(e))
    return false;
  }
}
