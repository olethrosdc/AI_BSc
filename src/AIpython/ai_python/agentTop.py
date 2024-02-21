# agentTop.py - Top Layer
# AIFCA Python code Version 0.9.12 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation
from typing import Dict, Tuple

from ai_python.agentEnv import Rob_body
# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2024 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from ai_python.display import Displayable
from ai_python.agentMiddle import Rob_middle_layer
from ai_python.agents import Environment
import matplotlib.pyplot as plt

class Rob_top_layer(Environment):
    def __init__(self, middle, timeout, locations):
        """middle is the middle layer
        timeout is the number of steps the middle layer goes before giving up
        locations is a loc:pos dictionary 
            where loc is a named location, and pos is an (x,y) position.
        """
        self.middle = middle
        self.timeout = timeout  # number of steps before the middle layer should give up
        self.locations = locations
        
    def do(self,plan):
        """carry out actions.
        actions is of the form {'visit':list_of_locations}
        It visits the locations in turn.
        """
        to_do = plan['visit']
        for loc in to_do:
            position = self.locations[loc]
            arrived = self.middle.do({'go_to':position, 'timeout':self.timeout})
            self.display(1,"Arrived at",loc,arrived)



class Plot_env(Displayable):
    def __init__(self, robot_body, robot_top):
        """sets up the plot
        """
        self.body = robot_body
        self.top = robot_top
        plt.ion()
        plt.axes().set_aspect('equal')
        self.redraw()

    def redraw(self):
        plt.clf()
        for wall in self.body.env.walls:
            ((x0,y0),(x1,y1)) = wall
            plt.plot([x0,x1],[y0,y1],"-k",linewidth=3)
        for loc in self.top.locations:
            (x,y) = self.top.locations[loc]
            plt.plot([x],[y],"k<")
            plt.text(x+1.0,y+0.5,loc) # print the label above and to the right
        plt.plot([self.body.rob_x],[self.body.rob_y],"go")
        plt.gca().figure.canvas.draw()
        if self.body.history or self.body.wall_history:
            self.plot_run()

    def plot_run(self):
        """plots the history after the agent has finished.
        This is typically only used if body.plotting==False
        """
        if self.body.history:
            xs,ys = zip(*self.body.history)
            plt.plot(xs,ys,"go")
        if self.body.wall_history:
            wxs,wys = zip(*self.body.wall_history)
            plt.plot(wxs,wys,"ro")


def setup_robot(
        environment: Environment,
        timeout: int = 200,
        locations: Dict[str, Tuple[int, int]] = None
):

    body = Rob_body(environment)
    middle = Rob_middle_layer(body)
    top = Rob_top_layer(middle,
                        timeout=timeout,
                        locations=locations
                        )

    return body, middle, top
