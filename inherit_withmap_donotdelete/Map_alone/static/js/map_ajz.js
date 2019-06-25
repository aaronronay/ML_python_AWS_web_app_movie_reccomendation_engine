function createMap(MovieTheaters) {
    // Create tile layer
    var streetMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.streets",
        accessToken: API_KEY
    });
    // Create baseMaps object to hold streetMap layer
    var baseMaps = {
        "Street Map": streetMap
    };
    // Create an overlayMaps object to hold the MovieTheaters layer
    var overlayMaps = {
        "Movie Theaters": MovieTheaters
    };
    // Create the map object
    console.log(user_data);
    var c_lat = user_data[0].user_lat;
    var c_lng = user_data[0].user_long;
    var map = L.map("map-id", {
        center: [c_lat, c_lng], // center = zipgeocode
        zoom: 12,
        layers: [streetMap, MovieTheaters]
    });
    // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
    }).addTo(map);
}

function createMarkers(response) {
    console.log(response);
    saved_data = response;
    user_data = response.User_Data;
    console.log(user_data)
    var theaters = response.Theaters;
    console.log(theaters);
    console.log(theaters.length);
    // Define array to hold created movie theatre markers
    var theaterMarkers = [];

    // Loop through the theaters array
    for (var index = 0; index < theaters.length; index++) {
        var theater = theaters[index];
        //for each theater, create a marker and bind a popup with the theater's name
        var theaterMarker = L.marker([theater.lat, theater.lng])
            .bindPopup("<h3>" + theater.Name + "<h3><h3>" + theater.Address + "<h3>");
        //add the marker to the theaterMarkers array
        theaterMarkers.push(theaterMarker);
    }
    // Create a layer group made from the theaterMarkers array, pass it into createMap function
    createMap(L.layerGroup(theaterMarkers));
}
//to format fetch with variables location and date

//d3.json("/scrape/" + location, createMarkers);
//d3.json("/scrape/" + location + "/" + date, createMarkers);

//fetch the json from the server at the route containing the webscrape
//d3.json("/scrape", createMarkers);
//d3.json("/scrape/" + location, createMarkers);



//var location = 44129
//d3.json("/scrape/" + location, createMarkers);
//d3.json("static/result"+ location + ".json", createMarkers);
d3.json("static/scrape/result.json", createMarkers);
//Temporary for test until webscrape data is available
//createMarkers();


// If json is formatted in GeoJSON format, format for fetch is similar to below
// d3.json('ne_110m_land.json', function(err, json) {
//     createMap(json);
//   })
