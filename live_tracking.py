import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Live Tracker", layout="wide")
st.title("📍 Live Location Tracker with Google Maps")

# Replace with your actual API key
google_api_key = "AIzaSyBUniW-P4OVS7-iprYSuyVOv5oXuzLI9Lc"

# Google Maps + JavaScript HTML inside Streamlit
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
      let map, marker;

      function initMap() {{
        const defaultLocation = {{ lat: 20.5937, lng: 78.9629 }};

        map = new google.maps.Map(document.getElementById("map"), {{
          center: defaultLocation,
          zoom: 5,
        }});

        const input = document.getElementById("search-box");
        const searchBox = new google.maps.places.SearchBox(input);

        map.addListener("bounds_changed", () => {{
          searchBox.setBounds(map.getBounds());
        }});

        searchBox.addListener("places_changed", () => {{
          const places = searchBox.getPlaces();
          if (places.length === 0) return;

          const place = places[0];
          if (!place.geometry) {{
            alert("No details available for input: " + place.name);
            return;
          }}

          // Fix: Set search box input value to place name or formatted address
          input.value = place.formatted_address || place.name || "";

          map.setCenter(place.geometry.location);
          map.setZoom(14);

          if (marker) marker.setMap(null);
          marker = new google.maps.Marker({{
            map,
            position: place.geometry.location,
            title: place.name,
          }});

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
                  map,
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

# Embed in Streamlit
html(map_html, height=700)
