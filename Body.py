import math
import numpy as np


class Body(object):
    dt = 10000 # timestep in seconds
    G = 6.67408e-11 # universal gravitational constant
    MASS_OF_SUN = 1.9885e30 # self explanatory, i know its kinda cheating but its easy

    def __init__(self, params):
        self.ap = np.array([0.0, 0.0])  # previous acceleration
        self.ac = np.array([0.0, 0.0])  # current acceleration
        self.an = np.array([0.0, 0.0])  # next acceleration

        self.M = float(params[0])  # set mass

        self.v = np.array([0.0, 0.0])  # create velocity and position vectors
        self.r = np.array([0.0, 0.0])

        self.r[0] = float(params[1])*1000  # set position
        self.r[1] = float(params[2])*1000
        self.r_init = self.r


    def update_position(self):
        # work out position using a_prev and a_current and velocity
        self.r = self.r + (self.v * self.dt) + ((1. / 6.) * ((4. * self.ac) - self.ap) * self.dt ** 2.)

        return self.r


    def init_velocity(self): # initialise velocity vector
        v = (math.sqrt((self.G * (self.MASS_OF_SUN + self.M ))/ self.r[0]))
        self.v = np.array([0.0, v])


    def update_velocity(self):  # work out new velocity using the position and all 3 accelerations

        self.v += ((1. / 6.) * ((2. * self.an) + (5. * self.ac) - self.ap) * self.dt)


    def shift_accelerations(self):  # sets previous acceleration to current and current to next
        self.ap = np.array(self.ac)
        self.ac = np.array(self.an)

    def orbit_check(self):
        if self.r[1] == self.r_init[1] and (self.r[0] > 0):
            return True

        return False
