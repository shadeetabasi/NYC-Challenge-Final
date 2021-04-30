// Creating our initial map object.
// We set the longitude, latitude, and the starting zoom level for sf.
// This gets inserted into the div with an id of 'map' in index.html.
var myMap = L.map("leafletmap", {
    center: [40.7128, -74.0060],
    zoom: 5,
  });
  
  // Adding a tile layer (the background map image) to our map
  // We use the addTo method to add objects to our map
  L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    tileSize: 512,
    maxZoom: 18,
    zoomOffset: -1,
    id: "mapbox.streets",
    accessToken: API_KEY
  }).addTo(myMap);
  // Store our API endpoint
// var queryUrl = "https://tree-map.nycgovparks.org/";
//  GET color radius call to the query URL
// d3.json(queryUrl, function(data) {
//   function styleInfo(feature) {
//     return {
//       opacity: 1,
//       fillOpacity: 1,
//       fillColor: getColor(feature.properties.mag),
//       color: "#000000",
//       radius: getRadius(feature.properties.mag),
//       stroke: true,
//       weight: 0.5
//     };
//   }
//   // set different color from magnitude
//     function getColor(magnitude) {
//     switch (true) {
//     case magnitude > 5:
//       return "#EA2C2C";
//     case magnitude > 4:
//       return "#EA822C";
//     case magnitude > 3:
//       return "#EE9C00";
//     case magnitude > 2:
//       return "#EECC00";
//     case magnitude > 1:
//       return "#D4EE00";
//     default:
//       return "#98EE00";
//     }
//   }
//   // set radiuss from magnitude
//     function getRadius(magnitude) {
//     if (magnitude === 0) {
//       return 1;
//     }
//     return magnitude * 4;
//   }
//     // GeoJSON layer
//     L.geoJson(data, {
//       // Maken cricles
//       pointToLayer: function(feature, latlng) {
//         return L.circleMarker(latlng);
//       },
//       // cirecle style
//       style: styleInfo,
//       // popup for each marker
//       onEachFeature: function(feature, layer) {
//         layer.bindPopup("Magnitude: " + feature.properties.mag + "<br>Location: " + feature.properties.place);
//       }
//     }).addTo(myMap);
//     // an object legend
//     var legend = L.control({
//       position: "bottomright"
//     });
//     // details for the legend
//     legend.onAdd = function() {
//       var div = L.DomUtil.create("div", "info legend");
//       var grades = [0, 1, 2, 3, 4, 5];
//       var colors = [
//         "#98EE00",
//         "#D4EE00",
//         "#EECC00",
//         "#EE9C00",
//         "#EA822C",
//         "#EA2C2C"
//       ];
//       // Looping through
//       for (var i = 0; i < grades.length; i++) {
//         div.innerHTML +=
//           "<i style='background: " + colors[i] + "'></i> " +
//           grades[i] + (grades[i + 1] ? "&ndash;" + grades[i + 1] + "<br>" : "+");
//       }
//       return div;
//     };
//     // Finally, we our legend to the map.
//     legend.addTo(myMap);
//   });