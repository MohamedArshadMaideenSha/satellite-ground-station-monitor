import requests
url="https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"
#Download Satellite TLE data from Celestrak
response=requests.get(url)
response.raise_for_status()  # Check for request errors 

#Save the TLE data to a local file
with open("station.text", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Download complete. TLE data saved to 'station.text'." \
"")
#Separating the TLE data into individual lines
line = response.text.strip().splitlines()

#Find ISS record in the TLE data
iss_index = next(
    (i for i, line in enumerate(line)
if "ISS ZARYA" in line.upper()),
    None
)
#Print ISS Name and Three Orbital Data Lines

if iss_index is not None:
    print("\nISS Satellite TLE Data:")
    for line in line[iss_index:iss_index + 4]:
        print(line)
else:
    print("\nISS ZARYA TLE data not found in the downloaded file.")
    for line in line[:3]:
        print(line)

#To find the orbit of the ISS, you can use the TLE data to calculate its position and velocity at a given time. This typically involves using a library like `sgp4` in Python, which can interpret TLE data and provide orbital parameters.

from skyfield.api import EarthSatellite, load, wgs84

stations=load.tle_file("station.text")
# Find the ISS satellite in the loaded TLE data
name={satellite.name: satellite for satellite in stations}
ISS=name.get("ISS ZARYA")

ts=load.timescale()
t=ts.now()

geocentric=ISS.at(t)
subpoint=wgs84.subpoint(geocentric)

print(f"\nISS Current Position:")
print(f"Latitude: {subpoint.latitude.degrees:.6f}°")
print(f"Longitude: {subpoint.longitude.degrees:.6f}°")
print(f"Altitude: {subpoint.elevation.m:.2f} meters")