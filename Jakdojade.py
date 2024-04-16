import json
import sys
import os
from dijkstra import go_dijkstra
from astar import go_astar
from astar_p import go_astar_p


class JakDojade:
    def __init__(self, graph_path, start_stop, end_stop, time_at_station, optimization=None):
        if not os.path.exists(graph_path):
            raise FileNotFoundError(f"File '{graph_path}' not found.")
        if optimization not in ['t', 'p', None]:
            raise ValueError("Optimization parameter must be 't' or 'p'")

        with open(graph_path, 'r', encoding='utf-8') as stops_graph_file:
            self.stops_graph = json.load(stops_graph_file)

        if start_stop not in self.stops_graph:
            raise ValueError(f"There is no stop with name [{start_stop}]")
        if end_stop not in self.stops_graph:
            raise ValueError(f"There is no stop with name [{end_stop}]")

        self.start_stop = start_stop
        self.end_stop = end_stop
        self.time_at_station = time_at_station
        self.opt = optimization

        self.path, self.cost, self.time = (None, None, None)

    def find_shortest_way(self):
        match self.opt:
            case None:
                self.path, self.cost, self.time = \
                    go_dijkstra(self.stops_graph, self.start_stop, self.end_stop, self.time_at_station)
            case 't':
                self.path, self.cost, self.time = \
                    go_astar(self.stops_graph, self.start_stop, self.end_stop, self.time_at_station)
            case 'p':
                self.path, self.cost, self.time = \
                    go_astar_p(self.stops_graph, self.start_stop, self.end_stop, self.time_at_station)
        self.display_results()

    def display_results(self):
        str_to_print = ""
        curr_line = None
        at_same_line_count = 1
        last_connection = None
        path_length = len(self.path)

        for index, connection in enumerate(self.path):
            if index != path_length-1:
                stop, dep_time, arr_time, line = connection
                if curr_line is None:
                    curr_line = line
                    str_to_print += f"\nLinia |{line}|:\n"\
                                    f"{stop} [{dep_time}] --"
                elif curr_line is line:
                    at_same_line_count += 1
                    last_connection = connection
                else:
                    str_to_print += f"({at_same_line_count})--> {stop} [{arr_time}]"
                    str_to_print += f"\nLinia |{line}|:\n"\
                                    f"{stop} [{dep_time}] --"
                    at_same_line_count = 1
                    curr_line = line
                    last_connection = connection
            else:
                stop = connection
                last_stop, dep_time, arr_time, line = last_connection
                str_to_print += f"({at_same_line_count})--> {stop} [{arr_time}]"

        print(str_to_print)
        print(f"Funkcja kosztu wynosi: [{self.cost}], "
              f"Czas znalezienia rozwiazania: [{self.time}]", file=sys.stderr)


def main():
    jakdojade1 = JakDojade('stops_graph.json', 'Kwiska', 'PL. GRUNWALDZKI', '24:00:00')
    jakdojade2 = JakDojade('stops_graph.json', 'Kwiska', 'PL. GRUNWALDZKI', '24:00:00', 't')
    jakdojade3 = JakDojade('stops_graph.json', 'Kwiska', 'PL. GRUNWALDZKI', '24:00:00', 'p')
    jakdojade4 = JakDojade('stops_graph.json', 'Magellana', 'DWORZEC AUTOBUSOWY', '24:00:00')
    jakdojade5 = JakDojade('stops_graph.json', 'Magellana', 'DWORZEC AUTOBUSOWY', '24:00:00', 't')
    jakdojade6 = JakDojade('stops_graph.json', 'Magellana', 'DWORZEC AUTOBUSOWY', '24:00:00', 'p')
    jakdojade1.find_shortest_way()
    jakdojade2.find_shortest_way()
    jakdojade3.find_shortest_way()
    jakdojade4.find_shortest_way()
    jakdojade5.find_shortest_way()
    jakdojade6.find_shortest_way()


if __name__ == "__main__":
    main()
