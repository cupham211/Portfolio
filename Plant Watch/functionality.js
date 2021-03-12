// filter taken from w3schools: https://www.w3schools.com/jquery/tryit.asp?filename=tryjquery_filters_table
$(document).ready(function(){
  $("#searchStores").on("keyup", function() {
    var region;
    if (document.getElementById('Abay').checked) {
      region = '#tableAbay';
    } else if (document.getElementById('Sbay').checked) {
        region = '#tableSbay';
    } else if (document.getElementById('Ebay').checked) {
        region = '#tableEbay';
    } else if (document.getElementById('Penin').checked) {
        region = '#tablePenin';
    } else if (document.getElementById('Nbay').checked) {
        region = '#tableNbay';
    } else {region = '#tableObay';}

    var value = $(this).val().toLowerCase();
    
    $(region + " tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });

  });
});
