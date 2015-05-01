import random
class ParticleAgent:
    def __init__(self, p_m, n_p, s_q, t_q, width, height):
        self.p_m = p_m
        self.n_p = n_p
        self.s_q = s_q
        self.t_q = t_q
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

    def sense(self, signal, agent):
        return
