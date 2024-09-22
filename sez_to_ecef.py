# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py lat_degrees long_degrees hae_km
# Converts SEZ to ECEF
# 
# Parameters:
#  lat_degrees: Latitude (deg)
#  long_degrees: Longitude (deg)
#  hae_km: Height above ellipsoid (km)
#  s_km
#  e_km
#  z_km
# Output:
#  Prints the ECEF x, y, z coordinates in km
#
# Written by Vineet Keshavamurthy
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

import sys 
import math


R_E_KM = 6378.1363
E_E = 0.081819221456


def calc_denom(ecc, latitude_rad):
  return math.sqrt(1.0 - ecc ** 2 * math.sin(latitude_rad)**2)

if len(sys.argv) != 7:
    print("Correct Number of Arguments not passed in")
    sys.exit(1)

# input variables
o_lat_deg = float(sys.argv[1])  # Latitude in degrees
o_lon_deg = float(sys.argv[2])  # Longitude in degrees
o_hae_km = float(sys.argv[3])   # Height above ellipsoid in km
s_km = float(sys.argv[4])       # SEZ s-component in km
e_km = float(sys.argv[5])       # SEZ e-component in km
z_km = float(sys.argv[6])       # SEZ z-component in km

# write script below this line

#convert latitude and longtitude to radians
latitude_rad = math.pi/180 * (o_lat_deg) #lat conversion to radians
longitude_rad = math.pi/180 * (o_lon_deg) #long conversion to radians

# Calculate the Ry matrix 
Ry_x = math.sin(latitude_rad)*s_km + (math.cos(latitude_rad))*z_km

Ry_y = e_km

Ry_z = z_km * math.sin(latitude_rad) - s_km * math.cos(latitude_rad)

#Complete 2nd Rotation
x_coord_ecef = Ry_x * math.cos(longitude_rad) - Ry_y * math.sin(longitude_rad)

y_coord_ecef = Ry_x * math.sin(longitude_rad) + Ry_y * math.cos(longitude_rad)

z_coord_ecef = Ry_z

denominator = calc_denom(E_E, latitude_rad)

#Calculate C_E
C_E = R_E_KM/denominator

#Calculate S_E
S_E = (R_E_KM * (1 - E_E**2))/denominator

#Calculate ECEF coordinates
R_x = (o_hae_km + C_E) * math.cos(latitude_rad) * math.cos(longitude_rad)
R_y = (o_hae_km + C_E) * math.cos(latitude_rad) * math.sin(longitude_rad)
R_z = (o_hae_km + S_E) * math.sin(latitude_rad)

# Identify ECEF coordinates
ecef_x_km = R_x + x_coord_ecef
ecef_y_km = R_y + y_coord_ecef
ecef_z_km = R_z + z_coord_ecef

# Print ECEF coordinates
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)