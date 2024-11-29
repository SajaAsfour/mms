import time
import API
from constants import *

class RightHandRule():
    def check_end_point(self, current_position):
        # Checks if the goal is reached
        return (current_position[0] == CENTER and current_position[1] == CENTER) or (
                current_position[0] == CENTER - 1 and current_position[1] == CENTER - 1) or (
                current_position[0] == CENTER - 1 and current_position[1] == CENTER) or (
                current_position[0] == CENTER and current_position[1] == CENTER - 1)

    def execute(self):
        API.log("RIGHT HAND RULE RUNNING...")

        current_position = [0, 0]
        orientation = 0  # 0 = North, 1 = East, 2 = South, 3 = West

        while True:
            # Check if the goal is reached
            if self.check_end_point(current_position):
                API.log("GOAL REACHED!")
                break

            # Turn right if there is no wall to the right
            if not API.wallRight():
                API.turnRight()
                orientation = (orientation + 1) % 4

            # Turn left if the front is blocked
            while API.wallFront():
                API.turnLeft()
                orientation = (orientation - 1) % 4

            # Move forward one step
            API.moveForward()

            # Update the position based on the orientation
            if orientation == 0:
                current_position[1] += 1  # Move up
            elif orientation == 1:
                current_position[0] += 1  # Move right
            elif orientation == 2:
                current_position[1] -= 1  # Move down
            elif orientation == 3:
                current_position[0] -= 1  # Move left

            # Mark the current position with red color
            API.setColor(current_position[0], current_position[1], 'R')
