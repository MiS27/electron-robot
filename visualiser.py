import numpy as np
import matplotlib.pyplot as plt
from action import Action

class Visualiser():

    __AGENT_AREA = np.pi * (15)**2

    __PARTICE_AREA = np.pi * (5)**2

    def __init__(self, environment):
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
        if event.key=='tab':
            action = Action.TAB
        if event.key=='escape':
            plt.close()
            return
        self.environment.run_action(action)
        self.draw()

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
            plt.scatter(pos[0], pos[1], s=Visualiser.__AGENT_AREA , alpha=0.5)
            plt.scatter(x, y, s=Visualiser.__PARTICE_AREA, alpha=0.5)
        plt.draw()
