
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Body import Body
from Satellites import Satellites
import random

G = 6.67408e-11
patches = []  # empty list for planets and sun
Bodies = []  # list to hold bodies
lim = 3e11


def generate_asteroid():  # generates asteroid with random parameters
    asteroid_v = np.array([0.0, random.uniform(10000,  20000)])
    # generates velocity vector for asteroid in positive direction

    asteroid_r = np.array([random.uniform(0, 3e11), 0.0])
    # position of doomsday asteroid on the x axis

    asteroid_m = 7.4e21  # typical mass of an asteroid
    asteroid = Satellites(asteroid_m, asteroid_v, asteroid_r)
    Bodies.append(asteroid)  # add asteroid to list of bodies
    patches.append(plt.Circle((asteroid.r[0], 0), lim * 0.01, color='black', animated=True))  # m



def total_kinetic_energy(Bodies):
    E = 0
    for body in Bodies:
        speed = abs(np.linalg.norm(body.v))  # works out speed of body
        E += 0.5 * body.M * (speed ** 2)  # kinetic energy of body

    E_file = open('KineticEnergy.txt', 'w')
    E_file.write(str(E))  # casts it to string and writes it to a file
    E_file.write("\n")
    E_file.close()


def total_gravitational_potential(Bodies):
    V = 0
    for body in Bodies:
        if body != Bodies[0]:
            distance = abs(np.linalg.norm(body.r - Bodies[0].r))  # works out distance
            V += -(G * Bodies[0].M * body.M) / distance  # Gpotential energy

    V_file = open('GPotentialEnergy.txt', 'w')
    V_file.write(str(V))  # casts to string and writes to file
    V_file.write("\n")
    V_file.close()


def force(b2, b1):  # works out force exterted on body2 by body1
    distance = np.linalg.norm(b2.r - b1.r)  # work out distance between bodies

    z = b2.r - b1.r  # result of b2-b1
    z_mag = abs(np.linalg.norm(z))  # magnitude of z

    unit = np.array([z[0] / z_mag, z[1] / z_mag])  # work out unit vector for 2->1

    f = ((-G * b1.M * b2.M) / distance ** 2.) * unit  # work out force exerted on body 2 by b1
    return f


def init_accelerations(Bodies):  # sets initial acceleration values
    for i in range(len(Bodies)):
        f = np.array([0.0, 0.0])  # initialise force vector
        for j in range(len(Bodies)):
            if i != j:
                f += force(Bodies[i], Bodies[j])  # work out force between one body and the rest

        Bodies[i].ap = f / Bodies[i].M  # work out acceleration and set it
        Bodies[i].ac = np.array(Bodies[i].ap)  # since this is initial current accel is also previous


def init_velocity(Bodies):  # sets intial velocity for all planetary bodies
    for body in Bodies[1:5]:
        body.init_velocity()


def next_accelerations(Bodies):  # work out next acceleration
    for i in range(len(Bodies)):
        f = np.array([0.0, 0.0])
        Bodies[i].shift_accelerations()  # functions to shift accelerations eg a_prev == a_current
        for j in range(len(Bodies)):
            if i != j:
                f += force(Bodies[i], Bodies[j]) # calcutes force one body is exerting on the other

        Bodies[i].an = f / Bodies[i].M  # calculates new acceleration


def animate(k):
    for i in range(len(patches)):
        e_orbits = 0  # number of times earth has orbited the sun

        r = Bodies[i].update_position()  # function to update position

        patches[i].center = (r[0], r[1])  # moves the patch representing the body

        next_accelerations(Bodies)  # calulates the next acceleration

        Bodies[i].update_velocity()  # for updates velocity for use in next iteration

        if k % 1000 == 0:
            total_kinetic_energy(Bodies)  # writes total kinetic energy of system
            total_gravitational_potential(Bodies)  # writes total GP energy of system


        if Bodies[3].orbit_check == True:
            e_orbits += 1
            print 'Orbits = %s' % e_orbits


        distance_e_a = abs(np.linalg.norm(Bodies[3].r - Bodies[5].r))
        #distance between earth and the asteroid
        if distance_e_a < (6.371e6*2):# check to see if asteroid is within double earths radius
            print "Asteroid has collided with earth."
            print "After %s seconds" % k*10000

    return patches


def Main():
    # read in Body params from 1 file
    # txt file format a body uses 5 lines:
    # mass
    # r1 x-coord
    # r2 y-coord
    bodies_file = "Bodies.txt"

    params = [line.rstrip('\n') for line in open(bodies_file)]  # parameters in string form

    # define all the bodies in simulation and initialise
    sun = Body(params[:3])
    mercury = Body(params[3:6])
    venus = Body(params[6:9])
    earth = Body(params[9:12])
    mars = Body(params[12:15])

    Bodies.append(sun)
    Bodies.append(mercury)
    Bodies.append(venus)
    Bodies.append(earth)
    Bodies.append(mars)  # add all bodies to a list

    init_velocity(Bodies)
    init_accelerations(Bodies)  # initialise accelerations

    fig = plt.figure()
    ax = plt.axes()

    patches.append(plt.Circle((0, 0), lim * 0.1, color='yellow', animated=True))  # sun
    patches.append(plt.Circle((mercury.r[0], 0), lim * 0.03, color='black', animated=True))  # mercury
    patches.append(plt.Circle((venus.r[0], 0), lim * 0.03, color='green', animated=True))  # venus
    patches.append(plt.Circle((earth.r[0], 0), lim * 0.03, color='blue', animated=True))  # earth
    patches.append(plt.Circle((mars.r[0], 0), lim * 0.03, color='red', animated=True))  # mars

    generate_asteroid()

    for i in range(len(patches)):
        ax.add_patch(patches[i])
    # adds bodies to plot


    ax.axis('scaled')  # sets up axes
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel('distance from sun (km)')
    ax.set_ylabel('distance from sun (km)')

    anim = FuncAnimation(fig, animate, frames=50000, repeat=False, interval=5, blit=True)

    plt.show()


Main()
