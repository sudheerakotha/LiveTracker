import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Live Tracker", layout="wide")
st.title("📍 Live Location Tracker with Google Maps")

# Use your own Google API Key here or set it in secrets.toml for production
google_api_key = "AIzaSyBUniW-P4OVS7-iprYSuyVOv5oXuzLI9Lc"

map_html = f"""
<!DOCTYPE html>
<html>
  <head>
    <style>
      #map {{
        height: 90vh;
        width: 100%;
      }}
      #search-box {{
        width: 300px;
        font-size: 16px;
        padding: 10px;
        margin: 10px;
        position: absolute;
        z-index: 5;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      }}
    </style>
  </head>
  <body>
    <input id="search-box" type="text" placeholder="Enter a city" />
    <div id="map"></div>

    <script>
      let map;
      let marker;

      function initMap() {{
        const defaultLocation = {{ lat: 20.5937, lng: 78.9629 }};

        map = new google.maps.Map(document.getElementById("map"), {{
          center: defaultLocation,
          zoom: 5,
        }});

        const input = document.getElementById("search-box");
        const searchBox = new google.maps.places.SearchBox(input);

        // Bias the SearchBox results towards current map's viewport.
        map.addListener('bounds_changed', () => {{
          searchBox.setBounds(map.getBounds());
        }});

        searchBox.addListener('places_changed', () => {{
          const places = searchBox.getPlaces();

          if (places.length === 0) {{
            return;
          }}

          const place = places[0];

          if (!place.geometry || !place.geometry.location) {{
            alert("No details available for input: " + place.name);
            return;
          }}

          // Center map to place location and zoom in
          map.setCenter(place.geometry.location);
          map.setZoom(14);

          // Remove old marker if exists
          if (marker) marker.setMap(null);

          // Add new marker at the place location
          marker = new google.maps.Marker({{
            map: map,
            position: place.geometry.location,
            title: place.name,
          }});

          // Optionally, update the search box value to formatted address or place name
          if (place.formatted_address) {{
            input.value = place.formatted_address;
          }} else if (place.name) {{
            input.value = place.name;
          }}

          startLiveTracking();
        }});
      }}

      function startLiveTracking() {{
        if (navigator.geolocation) {{
          navigator.geolocation.watchPosition(
            (position) => {{
              const pos = {{
                lat: position.coords.latitude,
                lng: position.coords.longitude,
              }};

              if (!marker) {{
                marker = new google.maps.Marker({{
                  map: map,
                  position: pos,
                  title: "You are here!",
                }});
              }} else {{
                marker.setPosition(pos);
              }}

              map.setCenter(pos);
            }},
            () => alert("Geolocation failed."),
            {{
              enableHighAccuracy: true,
              maximumAge: 0,
              timeout: 5000,
            }}
          );
        }} else {{
          alert("Your browser doesn't support geolocation.");
        }}
      }}
    </script>

    <script async defer
      src="https://maps.googleapis.com/maps/api/js?key={google_api_key}&libraries=places&callback=initMap">
    </script>
  </body>
</html>
"""

html(map_html, height=700)
