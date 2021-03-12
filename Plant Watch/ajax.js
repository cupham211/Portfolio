function postPut(reqType, obj, tableId, tabCode){
  var req = new XMLHttpRequest();

  req.onload = function() {
    if (req.status >= 200 && req.status < 400) {
      var response = JSON.parse(req.responseText);
      console.log(response);
      destroyTable(tableId);
      makeTable(response.stores, tableId);

    } else {
        console.log("Error in network request: " + req.statusText);
    }
};

    req.open(reqType, 'http://flip2.engr.oregonstate.edu:6969/plantwatch/'+ tabCode, true);
    // specify what kind of data is being sent to server
    req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    req.send(JSON.stringify(obj));
}

function getDelTable(reqType, tableId, tabCode, delId='') {
  var req = new XMLHttpRequest();

  req.onload = function() {
    if (req.status === 200) {
      var response = JSON.parse(this.responseText);
        console.log(response);
        destroyTable(tableId);
        makeTable(response.stores, tableId);


      } else {
        console.log("Error in network request: " + req.statusText);}
    }
      req.open(reqType, 'http://flip2.engr.oregonstate.edu:6969/plantwatch/'+ tabCode + delId, true);

    req.send(null);
}
