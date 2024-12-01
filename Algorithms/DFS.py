from constants import *
from Algorithms.Algorithm import Algorithm
import API

# Depth First Search (DFS) algorithm to navigate a maze. The maze is a set of paths that the robot can explore.
# Start at the robot’s position, and explore in one direction as far as possible.
# When encountering a dead-end or a previously visited spot, backtrack to explore other possible paths.
# Repeat the process until the goal is found.

class DFSRule(Algorithm):

    def execute(self):
        # Log the start of DFS execution
        API.log("DFS RUNNING...")

        # 0 > up, 1 > right, 2 > down, 3 > left
        orientation = 0
        current_position = [0, 0]  # Starting point

        stack = []  # Stack to keep track of the path for backtracking
        visited = set()  # Set to track visited nodes to prevent revisiting

        # Continue exploring until the goal (represented by '0') is found
        while MAZE_SETTINGS[current_position[0]][current_position[1]] != 0:

            self.update_maze_values()

            # Mark the current position as being visited by changing its color
            API.setColor(current_position[1], current_position[0], 'B')

            row, col = current_position
            front_wall = API.wallFront()
            right_wall = API.wallRight()
            left_wall = API.wallLeft()

            # Initialize neighboring nodes and their values
            neighbouring_nodes = [(), (), ()]
            neighbouring_values = [float("inf"), float("inf"), float("inf")]

            # Check the surrounding walls to identify possible directions
            self.check_walls_around(front_wall, left_wall, right_wall, col, neighbouring_nodes, orientation, row, neighbouring_values)

            # Skip this node if it has already been visited
            if (row, col) in visited:
                continue

            # Mark the current node as visited and add it to the stack
            visited.add((row, col))
            stack.append((row, col))

            # If a dead-end is reached (all directions blocked), backtrack
            if front_wall and right_wall and left_wall:
                if stack:
                    prev_row, prev_col = stack.pop()  # Backtrack to the previous position
                    current_position = [prev_row, prev_col]
                    continue

            # Explore the neighbors based on the lowest value (path to explore)
            lowest_neighbor = min(neighbouring_values)
            orientation = self.choose_lowest_neighbour(col, current_position, lowest_neighbor, stack, orientation, row, neighbouring_values)
            

        # Log when the DFS is completed
        API.log("FINISHED!!")

    def choose_lowest_neighbour(self, col, current_position, lowest_neighbor, stack, orientation, row, neighbouring_values):
        # Choose the next step based on the lowest neighbor value
        if lowest_neighbor == neighbouring_values[0]:  # Front
            API.moveForward()
            stack.append((row, col))  # Add current position to the stack

            # Update position based on current orientation
            if orientation == 0:
                current_position[0] += 1
            elif orientation == 1:
                current_position[1] += 1
            elif orientation == 2:
                current_position[0] -= 1
            elif orientation == 3:
                current_position[1] -= 1

        elif lowest_neighbor == neighbouring_values[1]:  # Right
            API.turnRight()
            API.moveForward()
            stack.append((row, col))  # Add current position to the stack

            # Update position and orientation when turning right
            if orientation == 0:
                current_position[1] += 1
                orientation = 1
            elif orientation == 1:
                current_position[0] -= 1
                orientation = 2
            elif orientation == 2:
                current_position[1] -= 1
                orientation = 3
            elif orientation == 3:
                current_position[0] += 1
                orientation = 0

        elif lowest_neighbor == neighbouring_values[2]:  # Left
            API.turnLeft()
            API.moveForward()
            stack.append((row, col))  # Add current position to the stack

            # Update position and orientation when turning left
            if orientation == 0:
                current_position[1] -= 1
                orientation = 3
            elif orientation == 1:
                current_position[0] += 1
                orientation = 0
            elif orientation == 2:
                current_position[1] += 1
                orientation = 1
            elif orientation == 3:
                current_position[0] -= 1
                orientation = 2

        return orientation

    def check_walls_around(self, front_wall, left_wall, right_wall, col, neighbouring_nodes, orientation, row, neighbouring_values):
        # Check the walls around the current position to find possible directions
        if not front_wall:
            if orientation == 0:
                front_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[0] = (row + 1, col)
            elif orientation == 1:
                front_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[0] = (row, col + 1)
            elif orientation == 2:
                front_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[0] = (row - 1, col)
            elif orientation == 3:
                front_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[0] = (row, col - 1)
            neighbouring_values[0] = front_val

        if not right_wall:
            if orientation == 0:
                right_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[1] = (row, col + 1)
            elif orientation == 1:
                right_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[1] = (row - 1, col)
            elif orientation == 2:
                right_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[1] = (row, col - 1)
            elif orientation == 3:
                right_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[1] = (row + 1, col)
            neighbouring_values[1] = right_val

        if not left_wall:
            if orientation == 0:
                left_val = MAZE_SETTINGS[row][col - 1]
                neighbouring_nodes[2] = (row, col - 1)
            elif orientation == 1:
                left_val = MAZE_SETTINGS[row + 1][col]
                neighbouring_nodes[2] = (row + 1, col)
            elif orientation == 2:
                left_val = MAZE_SETTINGS[row][col + 1]
                neighbouring_nodes[2] = (row, col + 1)
            elif orientation == 3:
                left_val = MAZE_SETTINGS[row - 1][col]
                neighbouring_nodes[2] = (row - 1, col)
            neighbouring_values[2] = left_val
