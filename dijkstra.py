import heapq
import time
from datetime import timedelta
from funcs import convert_time


def go_dijkstra(graph_dict, start_stop, end_stop, current_time):
    start_time = time.time()
    time_at_station = current_time

    def dijkstra(connections_graph, start, goal, curr_time):
        front = [(0, start)]
        came_from = {start: ()}
        cost_so_far = {start: 0}
        while front:
            _, current = heapq.heappop(front)

            if current == goal:
                break

            for neighbor in connections_graph[current]["end_stops"]:
                station_time = came_from[current][2] if came_from[current] else curr_time
                min_time, dep_time, arr_time, line = time_between_stops(current, neighbor, station_time)
                new_cost = cost_so_far[current] + min_time
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    heapq.heappush(front, (priority, neighbor))
                    came_from[neighbor] = (current, dep_time, arr_time, line)

        stop_path = []
        conn_info = []
        current = goal
        while current != start:
            stop_path.append(current)
            conn_info.append(came_from[current])
            current = came_from[current][0]
        stop_path.append(start)
        stop_path.reverse()
        conn_info.reverse()

        return stop_path, conn_info, cost_so_far[goal]

    def time_between_stops(start, end, curr_time):
        at_station_time = convert_time(curr_time)

        for neighbor, routes in graph_dict[start]["end_stops"].items():
            if neighbor == end:
                min_time_info = (float('inf'), "", "", "")
                min_time = timedelta(days=1000)
                for route, times in routes.items():
                    for time_slot in times:
                        dep_time = convert_time(time_slot["dep_time"])
                        arr_time = convert_time(time_slot["arr_time"])

                        if dep_time > at_station_time:
                            time_btw_stops = arr_time-dep_time
                            waiting_time = dep_time-at_station_time

                            if (time_btw_stops + waiting_time) <= min_time:
                                min_time = (time_btw_stops + waiting_time)
                                min_time_info = ((time_btw_stops + waiting_time).total_seconds() / 60,
                                                 time_slot["dep_time"], time_slot["arr_time"], route)
                return min_time_info

    path, route_info, cost = dijkstra(graph_dict, start_stop, end_stop, time_at_station)

    path_with_info = []
    for i, stop in enumerate(path[:-1]):
        current_stop_info = route_info[i]
        path_with_info.append((stop,) + current_stop_info[1:])
    path_with_info.append(end_stop)
    end_time = time.time()
    return path_with_info, cost, end_time - start_time
