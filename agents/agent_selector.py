#!/usr/bin/python3
from random import randint

# Debug imports
from pprint import pprint
from time import gmtime, strftime, localtime
import sys
import os
# python-sc2 imports
import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer

# agent imports
from loser_agent import *
from saferoach_agent import SafeRoachAgent
from zerglingBanelingRush_agent import SpawnPoolRavagerAgent

# Coloring for terminal output
# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# class Fitness(LoserAgent):
#     def __init__(self):
#         super().__init__()
#         print(bcolors.OKGREEN + "###Fitness Constructor" + bcolors.ENDC)
#         self.idle_workers = self.get_idle_workers

#     def __repr__(self):
#         return f"idle workers: {self.idle_workers}"

class AgentSelector(LoserAgent):
    def __init__(self, is_logging = False, isMainAgent = False):
        super().__init__(is_logging, "AgentSelector_", isMainAgent)

        print(bcolors.OKGREEN + "###AgentSelector Constructor" + bcolors.ENDC)

        # List of build orders
        self.agents = [SafeRoachAgent(), SpawnPoolRavagerAgent()]

        # Choose RandomBuild
        self.chooseRandomBuild()

        # List of strategies
        self.strategies = ["Aggressive", "Defensive"]

        # Choose RandomStrategy
        self.chooseRandomStrategy()

        # Properties
        self.stepsPerAgent = 100
        self.curAgentIndex = 0
        self.strategiesIndex = 0
        self.curStep = 0
        self.timesSwitched = 0

        # TODO
        # Call constructor for current agent
        # self.agents[self.curAgentIndex].__init__()

    def fitness(self):
        self.idle_workers = self.mainAgent.get_idle_workers

    def chooseRandomBuild(self):
        self.curAgentIndex = randint(0,1)
        print(bcolors.OKGREEN + "###RandomBuildIndex: {}".format(self.agents[self.curAgentIndex]) + bcolors.ENDC)

    def chooseRandomStrategy(self):
        self.strategiesIndex = randint(0,1)
        print(bcolors.OKGREEN + "###RandomStrategyIndex: {}".format(self.strategies[self.strategiesIndex]) + bcolors.ENDC)

    async def on_step(self, iteration):
        self.log("Step: %s Idle Workers: %s Overlord: %s Workers: %s" % (str(iteration), str(self.get_idle_workers), str(self.mainAgent.units(OVERLORD).amount), str(self.mainAgent.workers.amount)))

        # Run fitness on a certain number of steps
        if (iteration % self.stepsPerAgent == 0):
            print(bcolors.OKGREEN + "###Fitness function: {}".format(iteration) + bcolors.ENDC)
            self.fitness()

        # TODO
        # Call the current agent on_step
        await self.agents[self.curAgentIndex].on_step(iteration)

def main():
    # Start game with AgentSelector as the Bot, and begin logging
    sc2.run_game(sc2.maps.get("Abyssal Reef LE"), [
        Bot(Race.Zerg, AgentSelector(True, True)),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=False)

if __name__ == '__main__':
    main()

    # pysc2 old agent selector
    # def step(self, time_step):
    #     super().step(time_step)
    #
    #     self.curStep += 1
    #     if self.curStep == self.stepsPerAgent:
    #         self.curStep = 0
    #         self.curAgentIndex = (self.curAgentIndex + 1) % len(self.agents)
    #         self.agents[self.curAgentIndex].ResetBeliefState()
    #         self.timesSwitched += 1
    #
    #     return self.agents[self.curAgentIndex].step(time_step)
