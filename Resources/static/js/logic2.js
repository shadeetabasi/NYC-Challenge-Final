
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

// START CUSTOM LEGEND AND INTERACTIVITY HERE
// Adding interaction
function highlightFeature(e) {
  var layer = e.target;
  info.update(layer.feature.properties);

  layer.setStyle({
      weight: 5,
      color: '#666',
      dashArray: '',
      fillOpacity: 0.7
  });

  if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
      layer.bringToFront();
  }
}

function resetHighlight(e) {
  geojson.resetStyle(e.target);
  info.update();
}

// var geojson;
// // ... our listeners
// geojson = L.geoJson(...);

function zoomToFeature(e) {
  myMap.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
  layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      click: zoomToFeature
  });
}

geojson = L.geoJson(map_data, {
  style: style,
  onEachFeature: onEachFeature
}).addTo(myMap);

// Custom Control
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Average NYC Prices</h4>' +  (props ?
        '<b>' + props.postalCode + '</b><br />' + '$' + props.avg_price
        : 'Hover over a zipcode');
};

info.addTo(myMap);


// Set up the legend
var legend = L.control({position: 'bottomright'});

legend.onAdd = function () {

    var div = L.DomUtil.create('div', 'info legend'),
        prices = [100000, 200000, 500000, 600000, 800000, 1000000, 2000000],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < prices.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(prices[i] + 1) + '"></i> ' +
            prices[i] + (prices[i + 1] ? '&ndash;' + prices[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(myMap);