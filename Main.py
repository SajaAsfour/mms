import API
import heapq
import sys
import time
from constants import *
from Algorithms.Floodfill import FloodFill
from Algorithms.RightHand import RightHandRule
from Algorithms.LeftHand import LeftHandRule
from Algorithms.DFS import DFSRule


def color_center():
    API.setColor(CENTER, CENTER, "G")
    API.setColor(CENTER - 1, CENTER, "G")
    API.setColor(CENTER - 1, CENTER - 1, "G")
    API.setColor(CENTER, CENTER - 1, "G")


def main():

    API.log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "start")

    color_center()


    API.setText(CENTER, CENTER, "Goal")


    #floodfill = FloodFill()
    #leftHandRule = LeftHandRule()
    #rightHandRule = RightHandRule()
    dfs_algorithm = DFSRule()
    dfs_algorithm.execute()

    #floodfill.execute()
    #leftHandRule.execute()
    #rightHandRule.execute()







if __name__ == "__main__":
    main()
