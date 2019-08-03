var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var xhr = new XMLHttpRequest();
const fs = require('fs');

//get state
exports.getState = function() {
  botfileContents = fs.readFileSync('./bot.json', 'utf8')
  try {
    return JSON.parse(botfileContents)
  } catch(err) {
    console.error("Failed to parse bot.json")
    console.error(err)
    process.exit(1)
  }
}

//Missing dependencies, deactivated
//Get Link
exports.getMainLink = function(link, callback) {
  console.log("Fetching " + link);
  (async () => {
    //Nope
  })();
  //console.log(chalk.red("Failed to fetch: " + error))
}
