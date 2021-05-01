
// Creating map object
var myMap = L.map("leafletmap", {
  center: [40.7128, -74.0059],
  zoom: 11
});

// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);


// Grabbing our GeoJSON data..
// d3.json(link, function(data) {
//   // Creating a GeoJSON layer with the retrieved data
//   L.geoJson(nyc_map_data).addTo(myMap);
// });

function getColor(d) {
  return d > 2000000 ? '#800026' :
         d > 1000000  ? '#BD0026' :
         d > 800000  ? '#E31A1C' :
         d > 600000  ? '#FC4E2A' :
         d > 500000   ? '#FD8D3C' :
         d > 200000   ? '#FEB24C' :
         d > 100000   ? '#FED976' :
                    '#FFEDA0';
}

function style(feature) {
  return {
      fillColor: getColor(feature.properties.avg_price),
      weight: 2,
      opacity: 1,
      color: 'white',
      dashArray: '3',
      fillOpacity: 0.7
  };
}


L.geoJson(map_data, {style: style}).addTo(myMap);