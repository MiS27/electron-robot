import random
from scipy.stats import norm
class ParticleAgent:
    def __init__(self, p_m, n_p, c_p, s_q, t_q, p_r, r_m, color, width, height):
        self.p_m = p_m
        self.p_r = p_r
        self.r_m = r_m
        self.n_p = n_p
        self.n_r_p = int(n_p*c_p)
        self.s_q = s_q
        self.t_q = t_q
        self.color = color
        self.width = width
        self.height = height
        self.particles = []
        for i in range(n_p):
            self.particles.append((random.randint(0,width),random.randint(0,height)))

    def move(self, motion):
        particles = []
        for particle in self.particles:
            particles.append(((particle[0] + motion[0])%self.width,(particle[1] + motion[1])%self.height))
        self.particles = particles

    def __randomize_partice_position(self, x, y):
        if random.uniform(0, 1) <= self.p_r:
            motionX = random.randint(-self.r_m, self.r_m)
            motionY = random.randint(-self.r_m, self.r_m)
            x = (x + motionX)%self.width
            y = (y + motionY)%self.height
        return (x, y)

    def sense(self, transmissions):
        weights = []
        for particle in self.particles:
            w = 1
            for transmission in transmissions:
                transmitter = transmission[0]
                signal = transmission[1]
                p = 0
                for transmitterParticle in transmitter.particles:
                    p += norm.pdf(ParticleAgent.__distance(particle,transmitterParticle),loc = signal,scale = self.s_q*transmitter.t_q*10)
                p /= len(transmitter.particles)
                #print particle[0], particle[1], transmitterParticle[0], transmitterParticle[1], ParticleAgent.__distance(particle, transmitterParticle), signal, p
                w *= p
            weights.append(w)
        weights /= sum(weights)
        self.__resample(weights)
        return

    def __resample(self, weights):
        resampled = []
        mx = max(weights)
        b = 0
        inx = random.randint(0,self.n_p - 1)
        for i in range(self.n_p - self.n_r_p):
            b += random.uniform(0, 2*mx)
            while weights[inx] < b:
                b -= weights[inx]
                inx = (inx + 1) % self.n_p
            resampled.append(self.__randomize_partice_position(self.particles[inx][0], self.particles[inx][1]))
        for i in range(self.n_r_p):
            resampled.append((random.randint(0,self.width),random.randint(0,self.height)))

        self.particles = resampled
        return

    @staticmethod
    def __distance(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
