#!/usr/bin/python3
# William Zhang
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

ALTITUDE = 534
FOV_WIDTH = 1800
PERIOD = 1440
DIAMETER = 7917.5
RADIUS = DIAMETER / 2
E_VELOCITY = (2 * math.pi) / PERIOD


class Point():
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude * math.pi / 180
        self.longitude = longitude * math.pi / 180
        self.radius = RADIUS * math.cos(self.latitude)
        print(self.radius)

        self.x = self.radius * math.cos(0)
        self.y = self.radius * math.sin(0)
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
        #self.altitude = altitude
        self.period = period
        #self.orbital_radius = self.altitude + RADIUS
        #self.max_d =  (RADIUS + self.altitude - (RADIUS * math.cos(self.fov_width / RADIUS))) / math.sin(self.fov_width / RADIUS)
        print(RADIUS)
        self.x = RADIUS * math.cos(self.latitude)
        self.y = RADIUS * math.sin(0)
        self.z = RADIUS * math.sin(self.latitude)

    def __str__(self):
        return str((self.latitude, self.longitude))

    def __repr__(self):
        return str((self.latitude, self.longitude))

    def get_coords(self):
        return (self.x, self.y, self.z)

    def is_visible(self, point):
        ptx, pty, ptz = point.get_coords()
        satx, saty, satz = self.get_coords()
        d = dist(pty, ptx, saty, satx)
        
        return d <= (self.fov_width / 2)


#def dist(x1, y1, z1, x2, y2, z2):
#    return math.sqrt(abs(x1 - x2)**2 + abs(y1 - y2)**2 + abs(z1 - z2)**2)

def dist(y1, x1, y2, x2):
    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #R = 3958.76  # miles
    y1 *= math.pi / 180.0
    x1 *= math.pi / 180.0
    y2 *= math.pi / 180.0
    x2 *= math.pi / 180.0
    # approximate great circle distance with law of cosines
    return math.acos(math.sin(y1) * math.sin(y2) + math.cos(y1) * math.cos(y2) * math.cos(x2 - x1)) * RADIUS

def run(sat, pt):
    dists = []
    ts = []
    xp = []
    yp = []
    zp = []
    xs = []
    ys = []
    zs = []
    for t in range(PERIOD):
        pt.x = pt.radius * math.cos(E_VELOCITY * t)
        pt.y = pt.radius * math.sin(E_VELOCITY * t)

        sat_angular_velocity = (2 * math.pi) / sat.period
        
        sat.x += RADIUS * math.cos(sat_angular_velocity * t - sat.latitude)
        sat.z += RADIUS * -1 * math.sin(sat_angular_velocity * t - sat.latitude)
        print("Time: " + str(t) + " minutes", sat.is_visible(pt))
        
        #print("Sat: ", sat.get_coords())
        #print("DC: ", pt.get_coords())
        d = dist(pt.y, pt.x, sat.y, sat.x)
        print(d)
        # DATA COLLECTION #
        dists.append(d)
        ts.append(t)
        xp.append(pt.x)
        yp.append(pt.y)
        zp.append(pt.z)

        xs.append(sat.x)
        ys.append(sat.y)
        zs.append(sat.z)
        
    #plt.plot(ts, xs, zs)
    #plt.xlabel("Time (min)")
    #plt.ylabel("Distance between Satellite and Point (miles)")
    #plt.show()
    blank = [0] * len(ts)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xp = np.asarray(xp)
    yp = np.asarray(yp)
    zp = np.asarray(zp)

    ax.plot(xp, yp, zp)
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    zs = np.asarray(zs)

    ax.plot(xs, ys, zs)
    plt.show()


def main():
    lt = 38.9072
    lg = -77.0369
    sat = Satellite(lt, lg, ALTITUDE, 102, FOV_WIDTH)
    dc = Point("Washington DC", lt, lg)
    run(sat, dc)
    return 0


if __name__ == '__main__':
    main()
