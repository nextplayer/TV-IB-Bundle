function sendPostRequest(payload) {
  // ngrok url for flask
  var url = 'https://yourlink.ngrok-free.app';
  url += '/place_order';
  // var payload = { // trial run example
  //   symbol: "MES",
  //   action: "BUY",
  //   quantity: 1,
  //   type: "LMT",
  //   price: 5500
  // };

  var options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };

  var response = UrlFetchApp.fetch(url, options);
  Logger.log(response.getContentText());
}
