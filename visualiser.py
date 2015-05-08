import numpy as np
import matplotlib.pyplot as plt
from action import Action

class Visualiser():

    __AGENT_AREA = np.pi * (15)**2

    __PARTICE_AREA = np.pi * (2)**2

    def __init__(self, environment):
        self.signal = False
        self.environment = environment
        plt.ion()
        plt.axis([0,environment.width,0,environment.height])
        plt.connect('key_press_event', self.event)
        plt.show()
        self.draw()
        plt.pause(100)
        #self.fig.canvas.mpl_connect('key_press_event', event)


    def event(self, event):
        action = None
        #matplotlib.backend_bases.FigureCanvasBase(plt.gcf()).flush_events()
        if event.key=='up':
            action = Action.UP
        if event.key=='down':
            action = Action.DOWN
        if event.key=='right':
            action = Action.RIGHT
        if event.key=='left':
            action = Action.LEFT
        if event.key=='shift':
            action = Action.SHIFT
        if event.key=='escape':
            plt.close()
        if event.key=='x':
            self.signal = not self.signal
            self.draw()
        if action is not None:
            self.environment.run_action(action)
            self.draw()
        return

    def draw(self):
        plt.cla()
        plt.axis([0,self.environment.width,0,self.environment.height])
        for agent in self.environment.agents:
            pos = self.environment.agentPosition(agent)
            x = []
            y = []
            for particle in agent.particles:
                x.append(particle[0])
                y.append(particle[1])
            plt.scatter(pos[0], pos[1], c=agent.color, s=Visualiser.__AGENT_AREA , alpha=0.5)
            plt.scatter(x, y, c=agent.color, s=Visualiser.__PARTICE_AREA, alpha=0.5)
        if self.signal:
            self.drawSignals()
        plt.draw()

    def drawSignals(self):
        for transmission in self.environment.transmissions:
            agent = transmission[0]
            signal = transmission[1]
            (x, y) = self.environment.agentPosition(agent)
            line1 = [(x-signal, y),(x,y+signal)]
            line2 = [(x, y+signal),(x+signal,y)]
            line3 = [(x+signal, y),(x,y-signal)]
            line4 = [(x, y-signal),(x-signal,y)]
            (line1_xs, line1_ys) = zip(*line1)
            (line2_xs, line2_ys) = zip(*line2)
            (line3_xs, line3_ys) = zip(*line3)
            (line4_xs, line4_ys) = zip(*line4)
            plt.plot(line1_xs, line1_ys,color=agent.color, linewidth=1, linestyle='-', alpha = 1)
            plt.plot(line2_xs, line2_ys,color=agent.color, linewidth=1, linestyle='-', alpha = 1)
            plt.plot(line3_xs, line3_ys,color=agent.color, linewidth=1, linestyle='-', alpha = 1)
            plt.plot(line4_xs, line4_ys,color=agent.color, linewidth=1, linestyle='-', alpha = 1)
            plt.show()

