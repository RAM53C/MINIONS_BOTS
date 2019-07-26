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
    const browser = await puppeteer.launch({
      // Launch chromium using a proxy server on port 9876.
      // More on proxying:
      //    https://www.chromium.org/developers/design-documents/network-settings
      args: [ '--proxy-server=103.105.48.16:80' ]
    });
    const page = await browser.newPage();

    await page.goto(link);
    var html = await page.content();

    console.log(html); /* No Problem Mate */

    browser.close();
  })();
  //console.log(chalk.red("Failed to fetch: " + error))
}
