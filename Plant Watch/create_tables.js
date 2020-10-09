window.onload = function() {
  get_table();

  document.getElementsByName('tabs').forEach(function(e) {
      e.addEventListener("click", function() {
          get_table();
      });
  });

  document.getElementById('inputSubmit').addEventListener("click", function() {
    get_store_data();
  })
}

// destroy table----------------------------------------------------------------
function destroyTable(tableid, cont){
  var divcont = document.getElementById(tableid);
  var parent = divcont.parentNode;
  // if variable has contents
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }

  parent.appendChild(cont);
}

// make a table-----------------------------------------------------------------
function makeTable(res, container){

    container.innerHTML += `<form class="tr" id=${res._id}>
    <div class="td tdarea" id="area${res._id}" style="display:none;">${res.area}</div>
    <div class="td" id="store${res._id}">${res.store}</div>
    <div class="td" id="address${res._id}">${res.address}</div>
    <div class="td" id="website${res._id}" name=${res.website} onclick="openWebsite('${res.website}');"><a href="">${res.website}</a></div>
    <div class="td" id="restock_day${res._id}">${res.restock_day}</div>
    <div class="td editButtons"><input type="button" class="option inputEdit" id="edit${res._id}" onclick="editRow('${res._id}');" value="Edit">
    <input type="button" class="option inputUpdate" id="update${res._id}" style="display:none;" onclick="pkg_obj_row('${res._id}');" value="Update">
    <input type="button" class="option inputDelete" id="delete${res._id}" onclick="delRow('${res._id}');" value="Delete">
    <input type="button" class="option inputCancel" id="cancel${res._id}" style="display:none;" onclick="get_table();" value="Cancel"></div>
  </form>`;
}

// open websites----------------------------------------------------------------
function openWebsite(website) {
  window.open("https://"+ website, "_blank");
  event.preventDefault();
}

// edit row---------------------------------------------------------------------
function editRow(rowId){
    // display area of all stores
    var otherAreas = document.getElementsByClassName('tdarea');
    for (var i=0; i< otherAreas.length; i++){
      otherAreas[i].style.display="table-cell";
    }

    // show the area headers
    var th = document.getElementsByClassName("tharea");
    for (var i=0; i< th.length; i++){
      th[i].style.display="table-cell";
    }
    // switch out the option buttons
    document.getElementById("edit"+rowId).style.display="none";
    document.getElementById("update"+rowId).style.display="inline-block";
    document.getElementById("delete"+rowId).style.display="none";
    document.getElementById("cancel"+rowId).style.display="inline-block";

    // grab the cell values in the row
    var area = document.getElementById("area"+rowId);
    var store = document.getElementById("store"+rowId);
    var addy = document.getElementById("address"+rowId);
    var web = document.getElementById("website"+rowId);
    var restock = document.getElementById("restock_day"+rowId);

    var area_prev = area.innerHTML;
    var store_prev = store.innerHTML;
    var addy_prev = addy.innerHTML;
    var web_prev = web.getAttribute('name');
    var restock_prev = restock.innerHTML;

    // clear the old values
    area.innerHTML = "", store.innerHTML= "", addy.innerHTML = "", web.innerHTML = "", restock.innerHTML = "";

    // display values in input fields
    area.style.display="table-cell";
    area.innerHTML+= `<select name="area" id="inArea"+${rowId}>
            <option value="${area_prev}" selected>${area_prev}</option>
            <option value="South Bay">South Bay</option>
            <option value="East Bay">East Bay</option>
            <option value="Peninsula">Peninsula</option>
            <option value="North Bay">North Bay</option>
          </select> `;
    store.innerHTML += `<input list="storeName" id="inStore${rowId}" name="inStore" value="${store_prev}" />
    <datalist id="storeName">
      <option value="Safeway">
      <option value="Home Depot">
      <option value="Lowes">
      <option value="Trader Joes">
      <option value="Costco">
      <option value="Walmart">
      <option value="Ikea">
    </datalist>`;
    addy.innerHTML += `<input type="text" id="inAddy${rowId}" name="Addy" placeholder="House # Street, City" value="${addy_prev}">`;
    web.innerHTML += `<input type="text" id="inWeb${rowId}" placeholder="www.plantsite.com" value="${web_prev}">`;
    restock.innerHTML += `<input list="inRestock" id="Restock${rowId}" name="inRestock" value="${restock_prev}"/>
    <datalist id="inRestock">
      <option value="Unknown/Varies">
      <option value="Sunday">
      <option value="Monday">
      <option value="Tuesday">
      <option value="Wednesday">
      <option value="Thursday">
      <option value="Friday">
      <option value="Saturday">
    </datalist>`;

}

// package object in row-------------------------------------------------------
function pkg_obj_row(rowId){
  var getArea = document.getElementById("area"+rowId).firstChild;

  var formatRestock = document.getElementById("Restock"+rowId).value
  if (formatRestock != "Unknown/Varies") {
    formatRestock.toLowerCase();
    formatRestock = formatRestock.charAt(0).toUpperCase() + formatRestock.slice(1);
  }

  var row_obj = {
    _id: rowId,
    area: getArea.options[getArea.selectedIndex].text,
    store: document.getElementById("inStore"+rowId).value,
    website: document.getElementById("inWeb"+rowId).value,
    address: document.getElementById("inAddy"+rowId).value,
    restock_day: formatRestock
  };

  // send to put
  put_obj(row_obj);

  // switch out the option buttons
  document.getElementById("edit"+rowId).style.display="inline-block;";
  document.getElementById("update"+rowId).style.display="none;";
  document.getElementById("delete"+rowId).style.display="inline-block;";
  document.getElementById("cancel"+rowId).style.display="none;";
}

// Grab New Store Entry --------------------------------------------------------
function get_store_data() {
  var newArea = document.getElementById("inArea");

  var formatRestock = document.getElementById("Restock").value
  if (formatRestock != "Unknown/Varies") {
    formatRestock.toLowerCase();
    formatRestock = formatRestock.charAt(0).toUpperCase() + formatRestock.slice(1);
  }
  var new_store = {
    area: newArea.options[newArea.selectedIndex].text,
    store: document.getElementById("inStore").value,
    website: document.getElementById("inWeb").value,
    address: document.getElementById("inAddy").value,
    restock_day: formatRestock
  }
  // send to post function
  addStore(new_store);
}
