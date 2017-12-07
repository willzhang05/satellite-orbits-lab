#!/usr/bin/python3
# William Zhang
import math

ALTITUDE = 534
FOV_WIDTH = 1800
PERIOD = 102
DIAMETER = 7917.5
RADIUS = DIAMETER / 2
E_VELOCITY = (2 * math.pi) / 1440


class Point():
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude * math.pi / 180
        self.longitude = longitude * math.pi / 180
        self.radius = RADIUS * math.cos(self.latitude)

        self.x = self.radius * math.cos(self.longitude)
        self.y = self.radius * math.sin(self.longitude)
        self.z = RADIUS * math.sin(self.latitude)

    def __str__(self):
        return str((self.name, self.x, self.y, self.radius))

    def __repr__(self):
        return str((self.name, self.x, self.y, self.radius))

    def get_coords(self):
        return (self.x, self.y, self.z)
            

class Satellite():
    def __init__(self, latitude, longitude, altitude, period, fov_width):
        self.latitude = latitude * math.pi / 180
        self.longitude = longitude * math.pi / 180
        self.fov_width = fov_width
        self.altitude = altitude
        self.period = period
        self.orbital_radius = self.altitude + RADIUS
    
        self.x = self.orbital_radius * math.cos(self.longitude)
        self.y = RADIUS * math.sin(self.longitude)
        self.z = self.orbital_radius * math.sin(self.latitude)

    def __str__(self):
        #return str((self.x, self.y, self.z, self.period, self.fov_width, self.orbital_radius, self.angular_velocity))
        return str((latitude, longitude))

    def __repr__(self):
        return str((latitude, longitude))
        #return str((self.x, self.y, self.z, self.period, self.fov_width, self.orbital_radius, self.angular_velocity))

    def get_coords(self):
        return (self.x, self.y, self.z)

    def is_visible(self, point):
        ptx,pty,ptz = point.get_coords()
        satx,saty,satz = self.get_coords()
        d = dist(ptx, pty, ptz, satx, saty, satz)
        max_d = (RADIUS + self.altitude - (RADIUS * math.cos(self.fov_width / RADIUS))) / math.sin(self.fov_width / RADIUS)
        return d <= max_d


def dist(x1, y1, z1, x2, y2, z2):
    return math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2 + abs(z1-z2)**2)


def run(sat, pt):
    for t in range(PERIOD):
        pt.x += pt.radius * math.cos(E_VELOCITY * t)
        pt.y += pt.radius * math.sin(E_VELOCITY * t)

        print(sat.is_visible(pt))
        print("DC: ", pt.get_coords())
        sat_angular_velocity = (2 * math.pi) / sat.period
        sat.x += sat.orbital_radius * math.cos(sat_angular_velocity * t)
        sat.z += sat.orbital_radius * math.sin(sat_angular_velocity * t)
        print("Sat: ", sat.get_coords())
        print(dist(pt.x, pt.y, pt.z, sat.x, sat.y, sat.z))

def main():
    lt = 38.9072
    lg = -77.0369
    sat = Satellite(lt, lg, ALTITUDE, PERIOD, FOV_WIDTH)
    dc = Point("Washington DC", lt, lg)
    run(sat, dc)
    return 0

if __name__ == '__main__':
    main()
