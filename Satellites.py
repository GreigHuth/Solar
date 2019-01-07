from Body import Body

class Satellites(Body):
    # class to represent small bodies eg asteroids, satellites etc

    def __init__(self, M, v, r ):

        self.an = 0 # next accel
        self.ac = 0 # current accel
        self.ap = 0 # previous accel
        self.M = M # mass
        self.v = v # velocity vector
        self.r = r # position vector


