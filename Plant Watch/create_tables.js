window.onload = function() {
  getDelTable("GET",'tableAbay', -1);

  // tab onclick events
  document.getElementById('Abay').onclick = function() {getDelTable("GET",'tableAbay', -1);};
  document.getElementById('Sbay').onclick = function() {getDelTable("GET", 'tableSbay', 1);};
  document.getElementById('Ebay').onclick = function() {getDelTable("GET", 'tableEbay', 3);};
  document.getElementById('Penin').onclick = function() {getDelTable("GET", 'tablePenin', 4);};
  document.getElementById('Obay').onclick = function() {getDelTable("GET", 'tableObay', 5);};
  document.getElementById('Nbay').onclick = function() {getDelTable("GET", 'tableNbay', 2);};
  };

// destroy table----------------------------------------------------------------
function destroyTable(tableid){
  document.getElementById(tableid).innerHTML = '';
}

// make a table-----------------------------------------------------------------
function makeTable(json, tableID){
  var container = document.getElementById(tableID);
  var row = '';
  let tab = tableID[5];
  let regions = {1: '<option value="1">South Bay</option>',
                3: '<option value="2">East Bay</option>',
                4: '<option value="3">Peninsula</option>',
              2: '<option value="4">North Bay</option>',
              5: '<option value="5">Outside Bay</option>'}

  for (i=0; i<json.length; i++) {
    if (tableID == 'tableAbay') {
    row += `<tr><td>`;
  } else {
      row += `<tr><td class="colData" style="display:none;">`;
    }
    row += `<span class="${tab}${i}" id="staticArea${tab}${i}">${json[i].name}</span>
      <select class="col${tab}${i}" name="area" id="${tableID}Area${i}" style="display:none;">
    <option value="${json[i].area}" selected>${json[i].name}</option>`;

    for (var [key, value] of Object.entries(regions)){

      if (json[i].area != Number(key)) {
        row += regions[key];
      }
    }
          row +=  `</select></td>

            <td><span class="${tab}${i}" style="display:inline;">${json[i].storeName}</span>
            <input type="text" class="${tab}${i}" id="${tableID}Store${i}" style="display:none;" value='${json[i].storeName}'></td>
            <td><span class="${tab}${i}" style="display:inline;">${json[i].address}</span>
            <input type="text" class="${tab}${i}" id="${tableID}Address${i}" style="display:none;" value='${json[i].address}'></td>`;

    if (checkURL(json[i].website) && json[i].website.substring(0, 3) != 'http') {
        row +=
        ` <td><span class="${tab}${i}" style="display:inline;"><a onclick="openWebsite('${json[i].website}');">
  ${json[i].website}</a></span>`;

      } else if (checkURL(json[i].website) && json[i].website.substring(0, 3) == 'http') {
        row +=
        ` <td><span class="${tab}${i}" style="display:inline;"><a onlick="openWebsite(${json[i].website});">${json[i].website}</a></span>`;

      } else {
          row += `<td><span class="${tab}${i}" style="display:inline;">${json[i].website}</span>`;
      }

    row += `<input type="text" class="${tab}${i}" id="${tableID}Website${i}" style="display:none;" value='${json[i].website}'></td>
        <td><span class="${tab}${i}" style="display:inline;">${json[i].restockDay}</span>
        <input type="text" class="${tab}${i}" id="${tableID}Restock${i}" style="display:none;" value='${json[i].restockDay}'></td>
        <td><input type="button" class="option inputEdit" id="edit${tab}${i}" onclick="editRow('${tab}${i}', '${tableID}');" value="Edit">
        <input type="button" class="option inputUpdate" id="update${tab}${i}" style="display:none;" onclick="pkg_obj_row('${i}', ${json[i].storeID}, '${tableID}');" value="Update">
        <input type="button" class="option inputDelete" id="delete${tab}${i}" onclick="delRow(${json[i].storeID});" value="Delete">
        <input type="button" class="option inputCancel" id="cancel${tab}${i}" style="display:none;" onclick="lockTable('${tab}${i}', '${tableID}');" value="Cancel">
        </td>
        </tr>`;

  }
  container.innerHTML += row;
}
// lock the table from editing -------------------------------------------------
function lockTable(rowId, table) {
  var row = document.getElementsByClassName(rowId);
  let colArea = document.getElementsByClassName('colArea');
  let col = document.getElementsByClassName('col'+ rowId);
  let colD = document.getElementsByClassName('colData');

  for (i=0; i<colArea.length; i++){
    if (colArea[i].style.display == "table-cell"){
      colArea[i].style.display = 'none';
    }
  }

  for (i=0; i<col.length; i++){
    if (col[i].style.display == "none"){
      col[i].style.display = 'inline';
    } else {col[i].style.display = 'none';}
  }

  for (i=0; i<row.length; i++){
    if (row[i].style.display == "inline"){
      row[i].style.display = 'none';
    } else {
      row[i].style.display = "inline";
    }
  }

  // hide static area value in unlocked row
  if (table != 'tableAbay') {
    document.getElementById('staticArea'+ rowId).style.display = 'none';
  for (i=0; i<colD.length; i++){
    if (colD[i].style.display == "none"){
      colD[i].style.display = 'table-cell';
    } else {colD[i].style.display = 'none';}
  }
}


  // switch out the option buttons
  document.getElementById("edit"+rowId).style.display="inline-block";
  document.getElementById("update"+rowId).style.display="none";
  document.getElementById("delete"+rowId).style.display="inline-block";
  document.getElementById("cancel"+rowId).style.display="none";
}
// check if input is a valid website -------------------------------------------
function checkURL(site) {
  let url;

  if (site.substring(0, 3) != "http") {
    site = "https://" + site;
  }

  try {
    url = new URL(site);
  } catch (_) {
      return false;
  }

  return url.protocol === "http:" || url.protocol === "https:";
}
// open websites----------------------------------------------------------------
function openWebsite(website) {
  if (website.substring(0, 3) != "http") {
    website = "https://" + website;
  }
  window.open(website, "_blank");
  event.preventDefault();
}

// edit row---------------------------------------------------------------------
function editRow(rowId, table){

    var row = document.getElementsByClassName(rowId);
    let colArea = document.getElementsByClassName('colArea');
    let col = document.getElementsByClassName('col'+ rowId);
    let colD = document.getElementsByClassName('colData');

    // display the column header "Area"
    for (i=0; i<colArea.length; i++){
      if (colArea[i].style.display == 'none'){
        colArea[i].style.display = 'table-cell';
      }
    }

    for (i=0; i<row.length; i++){
      if (row[i].style.display == "none"){
        row[i].style.display = 'inline';
      } else {row[i].style.display = "none";}
    }

    // display select column data in "Area"
    for (i=0; i<col.length; i++){
      if (col[i].style.display == 'none'){
        col[i].style.display = 'inline';
      } else {col[i].style.display = 'none';}
    }

    // hide static area value in unlocked row
    if (table != 'tableAbay') {
      document.getElementById('staticArea'+ rowId).style.display = 'none';
    // unhide column data
    for (i=0; i<colD.length; i++){
      if (colD[i].style.display == "none"){
        colD[i].style.display = 'table-cell';
      } else {colD[i].style.display = 'none';}
    }
  }

    // switch out the option buttons
    document.getElementById("edit"+rowId).style.display="none";
    document.getElementById("update"+rowId).style.display="inline-block";
    document.getElementById("delete"+rowId).style.display="none";
    document.getElementById("cancel"+rowId).style.display="inline-block";

}

// get the tab code -----------------------------------------------------------
function getTabCodeTable(){
  var openTable = document.getElementsByName("tabs");
  let open, openTab;

  let tabKey = {"Abay": '-1', "Sbay": '1', "Ebay": '3', "Penin": '4', "Nbay": '2', "Obay":'5'};

  for (i=0; i< openTable.length; i++){
    if (openTable[i].checked) {
      openTab = tabKey[openTable[i].id];
      open = "table" + openTable[i].id;
      break;
    }
  }
  return [open, openTab]
}

// delete a store--------------------------------------------------------------
function delRow(storeId){

  let tabInfo = getTabCodeTable();
  storeId = '/' + storeId;

  // send to delete -----------------------------------------------------------
  getDelTable("DELETE", tabInfo[0], tabInfo[1], storeId);
}

// package object in row-------------------------------------------------------
function pkg_obj_row(rowId, storeId, tableId){

  let tabInfo = getTabCodeTable();

  var row_obj = {
    area: document.getElementById(tableId+'Area'+rowId).value,
    store: document.getElementById(tableId+'Store'+rowId).value,
    website: document.getElementById(tableId+'Website'+rowId).value,
    address: document.getElementById(tableId+'Address'+rowId).value,
    restock_day: document.getElementById(tableId+'Restock'+rowId).value,
    storeID: storeId
  };

  // send to put
  postPut("PUT", row_obj, tableId, tabInfo[1]);

  //close area column
  if (tableId != 'tableAbay') {
    let colArea = document.getElementsByClassName('colArea');
    for (i=0; i<colArea.length; i++){
      if (colArea[i].style.display == "table-cell"){
        colArea[i].style.display = 'none';
      }
    }
  }
}

// Grab New Store Entry --------------------------------------------------------
function get_store_data() {

  let tabInfo = getTabCodeTable();

  var new_store = {
    area: document.getElementById("inArea").value,
    store: document.getElementById("inStore").value,
    website: document.getElementById("inWeb").value,
    address: document.getElementById("inAddy").value,
    restock_day: document.getElementById("inRestock").value
  }
  // send to post function
  postPut("POST", new_store, tabInfo[0], tabInfo[1]);
  document.getElementById("add").reset();
}
