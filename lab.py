#!/usr/bin/python3
# William Zhang
import math

ALTITUDE = 534
FOV_WIDTH = 1800
PERIOD = 102
DIAMETER = 8000
LATITUDE = 39
EARTH_ANGULAR_VELOCITY = 4.375e-3


class Point():
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.radius = (DIAMETER / 2) * math.cos(latitude)

    def __str__(self):
        return str((self.name, self.x, self.y, self.radius))
    def __repr__(self):
        return str((self.name, self.x, self.y, self.radius))

    def get_coords(self):
        x = (DIAMETER / 2)*math.cos(latitude)*math.cos(longitude)
        y = (DIAMETER / 2)*math.sin(latitude)*math.sin(longitude)
        return (x, y)
            

class Satellite():
    def __init__(self, latitude, longitude, altitude, period, fov_width):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.period = period
        self.fov_width = fov_width
        self.orbital_radius = altitude + (DIAMETER / 2)
        self.angular_velocity = (2 * math.pi) / period
    
    def __str__(self):
        #return str((self.x, self.y, self.z, self.period, self.fov_width, self.orbital_radius, self.angular_velocity))
        return str((latitude, longitude))

    def __repr__(self):
        return str((latitude, longitude))
        #return str((self.x, self.y, self.z, self.period, self.fov_width, self.orbital_radius, self.angular_velocity))

    def get_coords(self):
        x = (DIAMETER / 2)*math.cos(latitude)*math.cos(longitude)
        y = (DIAMETER / 2)*math.sin(latitude)*math.sin(longitude)
        return (x, y)

def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def run(sat, pt):
    for t in range(PERIOD * 2):
        pt.x = pt.radius * math.cos(EARTH_ANGULAR_VELOCITY * t)
        pt.y = pt.radius * math.sin(EARTH_ANGULAR_VELOCITY * t)

        sat.x = sat.orbital_radius * math.cos(sat.angular_velocity * t)
        sat.y = sat.orbital_radius * math.sin(sat.angular_velocity * t)
        print(dist(pt.x, pt.y, sat.x, sat.y))

def main():
    lt = 38.9072
    lg = -77.0369
    sat = Satellite(lt, lg, ALTITUDE, PERIOD, FOV_WIDTH)
    dc = Point("Washington DC", lt, lg)
    run(sat, dc)
    return 0

if __name__ == '__main__':
    main()
