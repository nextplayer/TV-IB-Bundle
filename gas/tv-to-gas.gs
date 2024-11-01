function doPost(e) {
    try {
        // check if data received
        if (!e.postData || !e.postData.contents) {
            Logger.log("No data received in the POST request.");
            return ContentService.createTextOutput("No data received").setMimeType(ContentService.MimeType.TEXT);
        }

        // Parse the received JSON data
        var jsonData = JSON.parse(e.postData.contents);
        Logger.log("Received data: " + JSON.stringify(jsonData));
        // sheet.getRange(1, 2).setValue(JSON.stringify(jsonData)); // log parsed JSON data

        // check required fields in JSON data
        if (!jsonData.symbol || !jsonData.action || !jsonData.quantity || !jsonData.type || !jsonData.price) {
            Logger.log("Missing required fields in the data.");
            return ContentService.createTextOutput("Missing required fields").setMimeType(ContentService.MimeType.TEXT);
        }
        
        if (jsonData.symbol === 'ES1!') jsonData.symbol = 'MES';
        jsonData.action = jsonData.action.toUpperCase();
        
        // prepare payload
        var payload = {
          symbol: jsonData.symbol,
          action: jsonData.action,
          quantity: jsonData.quantity,
          type: jsonData.type,
          price: jsonData.price
        };

        sendPostRequest(payload); // send payload to IB

        Logger.log("Data processed successfully.");
        return ContentService.createTextOutput("Success").setMimeType(ContentService.MimeType.TEXT);
    } catch (error) {
        Logger.log("Error processing request: " + error.message);
        return ContentService.createTextOutput("Error: " + error.message).setMimeType(ContentService.MimeType.TEXT);
    }
}
