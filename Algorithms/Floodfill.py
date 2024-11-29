from constants import *
from Algorithms.Algorithm import Algorithm
import API

class FloodFill(Algorithm):
    """
    Implements the Flood-Fill algorithm to navigate through a maze
    by evaluating neighboring nodes and making decisions based on the
    shortest path cost.
    """

    def execute(self):
        """
        Main function that executes the Flood-Fill algorithm.
        """
        API.log("FLOODFILL RUNNING...")

        direction = 0  # Initial direction: 0=up, 1=right, 2=down, 3=left
        current_position = [0, 0]  # Starting position in the maze

        visited_nodes = []  # Stack to store nodes visited since the last decision
        decision_nodes = []  # List of decision nodes where choices were made

        # Continue navigating until the maze goal is reached (value 0 in maze settings)
        while MAZE_SETTINGS[current_position[0]][current_position[1]] != 0:
            self.update_maze_values()  # Update maze values to reflect costs dynamically

            # Mark the current cell as visited with a green color
            API.setColor(current_position[1], current_position[0], 'G')

            # Retrieve current position and wall information
            row, col = current_position
            front_wall = API.wallFront()
            right_wall = API.wallRight()
            left_wall = API.wallLeft()

            # Prepare placeholders for neighbors' positions and their costs
            neighbor_positions = [(), (), ()]  # Forward, right, left neighbors
            neighbor_values = [float("inf"), float("inf"), float("inf")]  # Default high cost for neighbors

            # Evaluate the surroundings and update neighbor positions and values
            self.evaluate_surroundings(
                front_wall, left_wall, right_wall, col, neighbor_positions, direction, row, neighbor_values
            )

            # Check if the current node is a decision node revisited
            if decision_nodes and (row, col) in decision_nodes:
                self.update_visited_nodes(col, visited_nodes, row)

            # Handle dead-end situations where all paths are blocked
            if left_wall and right_wall and front_wall:
                direction = self.handle_dead_end(
                    col, current_position, visited_nodes, direction, row
                )
                continue

            # Move toward the neighbor with the lowest cost
            lowest_neighbor_value = min(neighbor_values)
            direction = self.move_to_lowest_neighbor(
                col, current_position, lowest_neighbor_value, visited_nodes,
                direction, row, neighbor_values, neighbor_positions
            )

            # Check if the current node is a crossroad (multiple open paths)
            is_crossroad = (
                (not left_wall and not right_wall)
                or (not left_wall and not front_wall)
                or (not front_wall and not right_wall)
            )
            if is_crossroad:
                self.record_decision_node(col, decision_nodes, visited_nodes, row)

        API.log("FINISHED!!")

    def evaluate_surroundings(self, front_wall, left_wall, right_wall, col, neighbor_positions, direction, row, neighbor_values):
        """
        Evaluates the surroundings and updates neighbor positions and values.
        """
        # Check for open front wall and update corresponding neighbor
        if not front_wall:
            if direction == 0:
                neighbor_positions[0] = (row + 1, col)
                neighbor_values[0] = MAZE_SETTINGS[row + 1][col]
            elif direction == 1:
                neighbor_positions[0] = (row, col + 1)
                neighbor_values[0] = MAZE_SETTINGS[row][col + 1]
            elif direction == 2:
                neighbor_positions[0] = (row - 1, col)
                neighbor_values[0] = MAZE_SETTINGS[row - 1][col]
            elif direction == 3:
                neighbor_positions[0] = (row, col - 1)
                neighbor_values[0] = MAZE_SETTINGS[row][col - 1]

        # Check for open right wall and update corresponding neighbor
        if not right_wall:
            if direction == 0:
                neighbor_positions[1] = (row, col + 1)
                neighbor_values[1] = MAZE_SETTINGS[row][col + 1]
            elif direction == 1:
                neighbor_positions[1] = (row - 1, col)
                neighbor_values[1] = MAZE_SETTINGS[row - 1][col]
            elif direction == 2:
                neighbor_positions[1] = (row, col - 1)
                neighbor_values[1] = MAZE_SETTINGS[row][col - 1]
            elif direction == 3:
                neighbor_positions[1] = (row + 1, col)
                neighbor_values[1] = MAZE_SETTINGS[row + 1][col]

        # Check for open left wall and update corresponding neighbor
        if not left_wall:
            if direction == 0:
                neighbor_positions[2] = (row, col - 1)
                neighbor_values[2] = MAZE_SETTINGS[row][col - 1]
            elif direction == 1:
                neighbor_positions[2] = (row + 1, col)
                neighbor_values[2] = MAZE_SETTINGS[row + 1][col]
            elif direction == 2:
                neighbor_positions[2] = (row, col + 1)
                neighbor_values[2] = MAZE_SETTINGS[row][col + 1]
            elif direction == 3:
                neighbor_positions[2] = (row - 1, col)
                neighbor_values[2] = MAZE_SETTINGS[row - 1][col]

    def record_decision_node(self, col, decision_nodes, visited_nodes, row):
        """
        Records the current node as a decision node and resets visited nodes.
        """
        visited_nodes.append([])
        if (row, col) not in decision_nodes:
            decision_nodes.append((row, col))

    def update_visited_nodes(self, col, visited_nodes, row):
        """
        Updates the values of previously visited nodes to reflect cost increments.
        """
        previous_node = (row, col)
        for node in visited_nodes[-2]:  # Top of the stack
            MAZE_SETTINGS[node[0]][node[1]] = MAZE_SETTINGS[previous_node[0]][previous_node[1]] + 1
            previous_node = (node[0], node[1])

    def handle_dead_end(self, col, current_position, visited_nodes, direction, row):
        """
        Handles dead-end situations by turning around and backtracking.
        """
        API.turnRight()
        API.turnRight()
        API.moveForward()
        for visited in visited_nodes:
            visited.append((row, col))
        if direction == 0:
            current_position[0] -= 1
            direction = 2
        elif direction == 1:
            current_position[1] -= 1
            direction = 3
        elif direction == 2:
            current_position[0] += 1
            direction = 0
        elif direction == 3:
            current_position[1] += 1
            direction = 1
        return direction

    def move_to_lowest_neighbor(self, col, current_position, lowest_value, visited_nodes, direction, row, neighbor_values, neighbor_positions):
        """
        Moves to the neighboring node with the lowest cost and updates position and direction.
        """
        if lowest_value == neighbor_values[0]:  # Forward neighbor
            API.moveForward()
            for visited in visited_nodes:
                visited.append((row, col))
            if direction == 0:
                current_position[0] += 1
            elif direction == 1:
                current_position[1] += 1
            elif direction == 2:
                current_position[0] -= 1
            elif direction == 3:
                current_position[1] -= 1

        elif lowest_value == neighbor_values[1]:  # Right neighbor
            API.turnRight()
            API.moveForward()
            for visited in visited_nodes:
                visited.append((row, col))
            if direction == 0:
                current_position[1] += 1
                direction = 1
            elif direction == 1:
                current_position[0] -= 1
                direction = 2
            elif direction == 2:
                current_position[1] -= 1
                direction = 3
            elif direction == 3:
                current_position[0] += 1
                direction = 0

        elif lowest_value == neighbor_values[2]:  # Left neighbor
            API.turnLeft()
            API.moveForward()
            for visited in visited_nodes:
                visited.append((row, col))
            if direction == 0:
                current_position[1] -= 1
                direction = 3
            elif direction == 1:
                current_position[0] += 1
                direction = 0
            elif direction == 2:
                current_position[1] += 1
                direction = 1
            elif direction == 3:
                current_position[0] -= 1
                direction = 2
        return direction
