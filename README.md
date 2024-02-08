# **A* Pathfinding Simulator**

Welcome to the A* Pathfinding Simulator, a Python program using the Pygame library to visualize the A* pathfinding algorithm. This project provides an interactive environment where users can create and manipulate a grid, place start and end points, and observe the A* algorithm finding the shortest path between them.

## **Table of Contents**
- [**Introduction**](#introduction)
- [**Getting Started**](#getting-started)
- [**User Interface**](#user-interface)
- [**Usage**](#usage)
- [**Algorithm Details**](#algorithm-details)
- [**Contributing**](#contributing)
- [**License**](#license)

## **Introduction**

**A* Pathfinding Simulator** allows users to interactively create a grid and set start and end points. The A* algorithm is then applied to find the optimal path between the start and end points, considering obstacles or blocked nodes. This project aims to provide a visual representation of the A* algorithm and its efficiency in finding the shortest path.

## **Getting Started**

### **Prerequisites**
- Python 3.x
- Pygame library

### **Installation**
1. Clone the repository: `git clone https://github.com/your-username/astar-pathfinding-simulator.git`
2. Navigate to the project directory: `cd astar-pathfinding-simulator`
3. Install required dependencies: `pip install pygame`

## **User Interface**

The user interface consists of different screens, each serving a specific purpose:
1. **Intro Screen**: Displays the project title and a "Let's Go!!!" button to proceed.
2. **User Input Screen**: Allows users to input the size of the grid.
3. **Play Screen**: Provides a grid where users can set start and end points, block nodes, and initiate the A* algorithm.
4. **Endgame Screen**: Placeholder for future features or game completion.

## **Usage**

1. Run the program: `python pathfinding_simulator.py`
2. Follow the on-screen instructions to navigate through the screens.
3. On the Play Screen, use buttons to set start and end points, block nodes, and start the simulator.
4. Observe the A* algorithm in action, visualizing the pathfinding process.

## **Algorithm Details**

A* algorithm is a widely used pathfinding algorithm that efficiently finds the shortest path between two points on a grid. It intelligently evaluates potential paths based on a combination of actual cost (g) and estimated cost to the goal (h). The main steps include initializing open and closed sets, evaluating neighbors, and updating the path until the goal is reached.

## **Contributing**

If you'd like to contribute to the project, feel free to submit pull requests or open issues. Contributions and suggestions are welcome!

## **License**

This project is licensed under the [MIT License](LICENSE), allowing for both personal and commercial use.

Thank you for using the A* Pathfinding Simulator! Happy coding!
