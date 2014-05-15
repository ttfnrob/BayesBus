function clearOverlays() {
  for (var i = 0; i < markersArray.length; i++ ) {
    markersArray[i].setMap(null);
  }
  markersArray.length = 0;
}

function parseGeoJSON(text,sid,direction) {
  // The XMLHttpRequest response is JSON text - so parse it into an Object
  var json = JSON.parse(text);

  if (direction==="1") {
    var dirlab = " -";
  } else if (direction==="2") {
    var dirlab = " +";
  } else {
    var dirlab = "";
  }

  if (sid==="S1") {
    var icon = '/static/img/bus_purple.png';
  } else if (sid==="S2") {
    var icon = '/static/img/bus_blue.png';
  } else {
    var icon = '/static/img/bus_black.png';
  }

  options = {
    icon: icon,
    labelContent: sid+" "+dirlab,
    labelAnchor: new google.maps.Point(19, 53),
    labelClass: "service_label", // the CSS class for the label
    labelStyle: {opacity: 1.0}
  };

  var features = new GeoJSON(json, options);
  for (var i = 0; i < features.length; i++){
    markersArray.push(features[i]);
    features[i].setMap(map);
  }
}

function loadGeoJSON(sid) {
  var ts = Math.floor(Date.now()/1000);

  var xhr = new XMLHttpRequest();
  url = '/static/data/'+sid+'_1.json?ts='+ts;
  xhr.open('GET', url, true);
  xhr.onload = function() {
    parseGeoJSON(this.responseText,sid,"1");
  };
  xhr.send();

  var xhr = new XMLHttpRequest();
  url = '/static/data/'+sid+'_2.json?ts='+ts;
  xhr.open('GET', url, true);
  xhr.onload = function() {
    parseGeoJSON(this.responseText,sid,"2");
  };
  xhr.send();
}

function loadData() {
  // Clear markers and load a GeoJSON
  clearOverlays();
  loadGeoJSON(tracking_service);
  setTimeout(loadData,10000);
}

function initialize() {
  // Create a simple map.
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 11,
    center: {lat: 51.76, lng: -1.36}
  });

  loadData();

}

var map;
var markersArray = [];
google.maps.event.addDomListener(window, 'load', initialize);
