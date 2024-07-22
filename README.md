# Public Transport Route Finder

## Introduction
In this repository, we discuss two key algorithms in the field of pathfinding in graphs: Dijkstra's algorithm and A* (A-star) algorithm. Both these algorithms are widely used in various computer science domains, including robotics, artificial intelligence, and computer games, among others. Their applications include finding the shortest path between two points (nodes) in a graph, which can serve multiple purposes across various domains and applications, from gaming to logistics.

![image](https://github.com/user-attachments/assets/d1aa3343-b039-48cc-b3be-ef818a1c4da3)
![image](https://github.com/user-attachments/assets/1c029a6c-df88-4a4f-83b5-e72dea901267)
![image](https://github.com/user-attachments/assets/70900f9d-6f3d-4e73-ab47-bfa60c408a7a)

### Algorithms:
- **Dijkstra's Algorithm**: Dijkstra's algorithm finds the shortest paths from a selected vertex to all other vertices in a weighted graph, where edge weights represent the cost of transitioning between them.
- **A* Algorithm**: A* algorithm utilizes a similar approach but with an additional heuristic, allowing for more efficient graph traversal by considering the estimated distance to the goal.

## Program Logic and Code Structure

### Assumptions and Considerations:
- The graph is assumed to be unidirectional due to not all stops having reverse connections in the provided `connection_graph.csv` file.
- To maintain connectivity to stops like "Żórawina (Mostek)", which might not have outbound connections, connections to such stops are always checked.
- Stops with the same name but different coordinates are considered connected, simplifying the graph by adding the first occurrence of such stops.
- To incorporate multiple criteria, their values are summed rather than compared as tuples, ensuring equal importance for all criteria.

### Program Logic:
The `JakDojade` class is responsible for finding the shortest route between two stops in the public transport network. It consists of several key methods and variables, storing information about the stop graph, start and end points of the route, time spent at stops, and optimization criteria (if provided).

- **`__init__`**: Initializes class attributes based on provided parameters, validating the path to the graph file and the optimization parameter.
- **`find_shortest_way`**: Finds the shortest route between the specified stops. Based on the optimization criteria (if provided), it selects the appropriate algorithm (Dijkstra or A*) to find the route and displays the results using the `display_results` method.
- **`display_results`**: Displays the found route in a readable text format, including line numbers and departure/arrival times at each stop, along with the cost and time spent on finding the route.

### Code:
The code consists of the `JakDojade` class and auxiliary functions imported from separate modules (`dijkstra.py`, `astar.py`, and `astar_p.py`). It follows a modular structure to handle different aspects of route finding.

## Helper Files and Preprocessing

### Helper File: `funcs.py`
The `funcs.py` file contains the `convert_time` function, which converts time from text format to a Python datetime object. It parses the time into hours, minutes, and seconds, handles cases where the hour exceeds 24, and returns the time object in the appropriate format.

### Preprocessing `connection_graph.csv`
The `connection_graph.csv` file is processed using the `Graph` class, converting the CSV file into a graph structure represented as a dictionary and saving it to a JSON file. The preprocessing involves:
1. Reading data from the CSV file using the `pandas` library.
2. Creating an empty dictionary `graph_dict` to represent the graph.
3. Iterating through each row of the DataFrame, extracting information about lines, start and end stops, geographic coordinates, and departure/arrival times.
4. Checking if the start stop is already in `graph_dict` and adding a key for it if not, along with information about its end stops and coordinates.
5. Adding information about departure and arrival times for each line between stops.
6. Saving the obtained dictionary to a JSON file named `stops_graph.json`.

## Results and Analysis

### Sample Results:
- Results for routes from 'Kwiska' to 'PL. GRUNWALDZKI' at 09:00:00 and from 'Magellana' to 'DWORZEC AUTOBUSOWY' at 11:00:00 are provided for both Dijkstra and A* algorithms, with and without considering transfers.
- The results display the route with line numbers, departure/arrival times at each stop, along with the cost and time taken to find the solution.

### Analysis:
- Both Dijkstra and A* algorithms perform well in finding routes in Wroclaw's stop network, with A* demonstrating better speed performance.
- A* algorithm proves particularly efficient, especially in scenarios like nighttime tram rides, possibly due to reduced traffic and fewer connections to consider.
- Considering both travel time and transfers, A* with additional optimization criteria provides a good balance between speed and minimizing transfers.
- While the program's solution-finding time may not be optimal for real-time applications, it serves as valuable training to understand similar algorithms and their potential applications.

## Conclusion
The repository provides implementations of Dijkstra and A* algorithms for finding routes in a public transport network, along with preprocessing steps and analysis of results. While both algorithms perform well, A* stands out for its efficiency, especially with additional optimization criteria. The project serves as a valuable learning experience in understanding and applying pathfinding algorithms in practical scenarios.
