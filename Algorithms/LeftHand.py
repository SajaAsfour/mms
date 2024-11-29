import time
import API
from constants import *

class LeftHandRule():
    def check_end_point(self, current_position):
        # Checks if the goal is reached
        return (current_position[0] == CENTER and current_position[1] == CENTER) or (
                current_position[0] == CENTER - 1 and current_position[1] == CENTER - 1) or (
                current_position[0] == CENTER - 1 and current_position[1] == CENTER) or (
                current_position[0] == CENTER and current_position[1] == CENTER - 1)

    def execute(self):
        API.log("LEFT HAND RULE RUNNING...")

        current_position = [0, 0]
        orientation = 0  # 0 = North, 1 = East, 2 = South, 3 = West

        while True:
            # Check if the goal is reached
            if self.check_end_point(current_position):
                API.log("GOAL REACHED!")
                break

            # Turn left if there is no wall to the left
            if not API.wallLeft():
                API.turnLeft()
                orientation = (orientation - 1) % 4

            # Turn right if the front is blocked
            while API.wallFront():
                API.turnRight()
                orientation = (orientation + 1) % 4

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

            # Mark the current position with blue color
            API.setColor(current_position[0], current_position[1], 'B')
