# coding: utf-8
import random
from action import Action
from itertools import cycle
from agents.particle import ParticleAgent
from agents.known import KnownAgent

class Env:
    __MOTIONS = {
        Action.UP : (0, 1),
        Action.DOWN : (0, -1),
        Action.LEFT : (-1, 0),
        Action.RIGHT : (1, 0)
    }
    """Wartosci o jakie zmieniaja sie wspolrzedne agenta po wykonaniu deterministycznych akcji."""

    def __init__(self, path):
        """Tworzy srodowisko na podstawie opisu z pliku. Plik powinien miec nastepujacy format:
        <height> <width>
        <n>
        <d> <c> <p_m> <t_q> <n_p> <c_p> <s_q> <p_r> <r_m>
        d - czy wie gdzie jest;
        c - color
        p_m - prawdopodobienstwo ruchu
        t_q - jakość transmisji o ile sygnał danego transmitera może być zły
        n_p - liczba cząsteczek
        c_p - procent czastek ktore umieraja
        s_q - jakość odbiornika; o ile sygnał może być źle odczytany
        p_r - prawdopodobienstwo szumu czasteczki
        r_m - wielkosc szumu czasteczki

        Argument path to sciezka do pliku zawierajacego opis srodowiska."""

        file = open(path, 'r')

        tokens = file.readline().strip().split()
        self.height = int(tokens[0])
        self.width = int(tokens[1])

        self.n = int(file.readline().strip())
        self.agentsInfo = {}
        self.agents = []
        self.transmissions = None

        for i in range(self.n):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            tokens = file.readline().strip().split()
            d = 1 == int(tokens[0])
            c = tokens[1]
            p_m = float(tokens[2])
            t_q = float(tokens[3])
            agent = None
            n_p = 1
            s_q = 1.0
            if d is not True:
                n_p = int(tokens[4])
                c_p = float(tokens[5])
                s_q = float(tokens[6])
                p_r = float(tokens[7])
                r_m = float(tokens[8])
                agent = ParticleAgent(p_m, n_p, c_p, s_q, t_q, p_r, r_m, c, self.width, self.height)
            else:
                agent = KnownAgent(x, y, p_m, t_q, c, self.width, self.height)
            self.agents.append(agent)
            self.agentsInfo[agent] = {"x" : x, "y" : y, "d" : d, "p_m" : p_m, "t_q" : t_q, "s_q" : s_q}
        self.cycleAgents = cycle(self.agents)
        self.currentAgent = next(self.cycleAgents)
        file.close()
        self.__send_signal()
        return

    def __send_signal(self):
        """Aktualizuje stan sensora aktualnego agenta."""
        transmissions = []
        for agent in self.agents:
            if agent is not self.currentAgent:
                agentInfo = self.agentsInfo[agent]
                currentAgentInfo = self.agentsInfo[self.currentAgent]
                distance = abs(agentInfo["x"] - currentAgentInfo["x"]) + abs(agentInfo["y"] - currentAgentInfo["y"])

                signal = random.uniform(agentInfo["t_q"], 2 - agentInfo["t_q"]) * random.uniform(currentAgentInfo["s_q"], 2 - currentAgentInfo["s_q"]) * distance
                transmissions.append((agent, signal))
        self.currentAgent.sense(transmissions)
        self.transmissions = transmissions

    def __move_agent(self, agent, motion):
        agentInfo = self.agentsInfo[agent]
        agentInfo["x"] = (agentInfo["x"] + motion[0])%self.width
        agentInfo["y"] = (agentInfo["y"] + motion[1])%self.height
        agent.move(motion)

    def __randomize_agent_position(self, agent):
        agentInfo = self.agentsInfo[agent]
        if random.uniform(0, 1) >= agentInfo["p_m"]:
            motion = random.choice(Env.__MOTIONS.values())
            self.__move_agent(agent, motion)
        return

    def agentPosition(self, agent):
        #return (random.uniform(0,100),random.uniform(0,100))
        return (self.agentsInfo[agent]["x"],self.agentsInfo[agent]["y"])

    def run_action(self, action):
        if action is Action.SHIFT:
            self.currentAgent = next(self.cycleAgents)
        else:
            motion = list(Env.__MOTIONS[action])
            self.__move_agent(self.currentAgent, motion)
        self.run()
        return

    def run(self):
        """Zmienia pozycje agentow w sposob losowy i aktualizuje sensor aktualnego agenta"""
        for agent in self.agents:
            self.__randomize_agent_position(agent)
        self.__send_signal()
