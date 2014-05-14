function deleteMarkers() {
  
}

function loadData() {
  // Clear markers and load a GeoJSON
  var ts = Math.floor(Date.now()/1000);
  // console.log("Reloading geoJSON with ts "+ts);
  deleteMarkers();
  map.data.loadGeoJson('static/data/S1_1.json?ts='+ts);
  map.data.loadGeoJson('static/data/S1_2.json?ts='+ts);
  map.data.loadGeoJson('static/data/S2_1.json?ts='+ts);
  map.data.loadGeoJson('static/data/S2_2.json?ts='+ts);
  setTimeout(loadData,5000);
}

function initialize() {
  // Create a simple map.
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 11,
    center: {lat: 51.76, lng: -1.36}
  });

  var imgS1_1 = 'http://gmaps-samples.googlecode.com/svn/trunk/markers/green/marker1.png';
  var imgS1_2 = 'http://gmaps-samples.googlecode.com/svn/trunk/markers/red/marker1.png';
  var imgS2_1 = 'http://gmaps-samples.googlecode.com/svn/trunk/markers/green/marker2.png';
  var imgS2_2 = 'http://gmaps-samples.googlecode.com/svn/trunk/markers/red/marker2.png';

  map.data.setStyle(function(feature) {
    var service = feature.getProperty('service');
    if (service==="S1") {
      return ({ icon: imgS1_1 });
    }
    if (service==="S2") {
      return ({ icon: imgS2_2 });
    }
  });

   map.data.addListener('click', function(event) {
    console.log(event.feature);
  });

  loadData();

}

var map;
var markers = [];
google.maps.event.addDomListener(window, 'load', initialize);
