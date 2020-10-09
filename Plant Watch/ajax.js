//GET request-------------------------------------------------------------------
function get_table() {
  var grab, query, cont;
  var tabs = document.getElementsByName('tabs');

// reset headers as needed
  var tharea= document.getElementsByClassName("tharea");
  for (var i=0; i< tharea.length; i++){
      tharea[i].style.display = "none";
  }
  for (var i=0; i < tabs.length; i++){
    if (tabs[i].checked){
      grab = tabs[i].id;
    }
  }

  if (grab == "Sbay") {
    query = "South Bay";
  } else if (grab == "Ebay") {
    query = "East Bay";
  } else if (grab == "Penin") {
    query = "Peninsula";
  } else {query = "North Bay";}

  var tableid = 'fill'+ grab;

  var req = new XMLHttpRequest();

  req.onload = function() {
    if (req.status === 200) {
      var response = JSON.parse(this.responseText);

      cont = document.createElement("div");
      cont.className = "tbody";
      cont.id = tableid;

        destroyTable(tableid, cont);

        //response[i].keyword to reference diff items in obj
        for(var i=0; i< response.length; i++){
          makeTable(response[i], cont);
        }
      } else {
        console.log("Error in network request: " + req.statusText);}
    }
      req.open("GET", 'https://cors-anywhere.herokuapp.com/https://warm-mesa-37033.herokuapp.com/?area='+ query, true);


    req.send(null);
}


// PUT function-----------------------------------------------------------------
function put_obj(update){
  var req = new XMLHttpRequest();

  req.onload = function() {
    if (req.status >= 200 && req.status < 400) {

      var response = JSON.parse(req.responseText);
      console.log(response);
      get_table();

    } else {
        console.log("Error in network request: " + req.statusText);
    }
};

    req.open('PUT', 'https://cors-anywhere.herokuapp.com/https://warm-mesa-37033.herokuapp.com/'+update._id, true);
    // specify what kind of data is being sent to server
    req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    req.send(JSON.stringify(update));
    event.preventDefault();
}


// DELETE function--------------------------------------------------------------
function delRow(rowId) {
  var req = new XMLHttpRequest();

  req.onload = function() {
    if (req.status === 200) {
      var response = JSON.parse(this.responseText);
      console.log(response);
      get_table();

    } else {
      console.log("Error in network request: " + req.statusText);}
  }
    req.open("DELETE", 'https://cors-anywhere.herokuapp.com/https://warm-mesa-37033.herokuapp.com/'+rowId, true);

  req.send(null);
}


// POST data--------------------------------------------------------------------
function addStore(store_Obj) {
  var req = new XMLHttpRequest();

  req.onload = function() {
    if (req.status >= 200 && req.status < 400) {
      var response = JSON.parse(req.responseText);
      console.log(response);

      document.getElementById("add").reset();
      get_table();

    } else {
        console.log("Error in network request: " + req.statusText);
    }
};

    req.open('POST', 'https://cors-anywhere.herokuapp.com/https://warm-mesa-37033.herokuapp.com/', true);
    // specify what kind of data is being sent to server
    req.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    req.send(JSON.stringify(store_Obj));
    event.preventDefault();
}
