
lat1 = float(input("Enter the latitude of the first location: "))
long1 = float(input("Enter the longitude of the first location: "))
lat2 = float(input("Enter the latitude of the second location: "))
long2 = float(input("Enter the longitude of the second location: "))

# Example: https://www.gpskoordinaten.de/
# Frankfurt: lat=50.1109, long=8.6821
# Paris: lat=48.8534951, long=2.3483915
# Distance=445.55

distance = 69 * ((lat1-lat2)**2 + (long1-long2)**2)**0.5
print("The distance is:", distance)
