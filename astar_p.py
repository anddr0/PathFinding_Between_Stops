import heapq
import time
import math
from datetime import timedelta
from funcs import convert_time


def go_astar_p(graph_dict, start_stop, end_stop, current_time):
    start_time = time.time()
    time_at_station = current_time

    def astar(connections_graph, start, goal, heuristic_fn, curr_time):
        front = [(0, start)]
        came_from = {start: ()}
        cost_so_far = {start: 0}
        while front:
            _, current = heapq.heappop(front)

            if current == goal:
                break

            for neighbor in connections_graph[current]["end_stops"]:
                station_time = came_from[current][2] if came_from[current] else curr_time
                prev_line = came_from[current][-1] if came_from[current] else None
                min_time, dep_time, arr_time, line = time_between_stops(current, neighbor, station_time, prev_line)
                new_cost = cost_so_far[current] + min_time
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic_fn(goal, neighbor)
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

    def get_stop_lines(stop):
        lines = set()
        for neighbor, routes in graph_dict[stop]["end_stops"].items():
            for route, _ in routes.items():
               lines.add(route)
        return lines

    def time_between_stops(start, end, curr_time, prev_line):
        at_station_time = convert_time(curr_time)

        start_stop_lines = get_stop_lines(start)
        end_stop_lines = get_stop_lines(end_stop)
        common_lines = start_stop_lines.intersection(end_stop_lines)

        for neighbor, routes in graph_dict[start]["end_stops"].items():
            if neighbor == end:
                min_time_info = (float('inf'), "", "", "")
                min_time = timedelta(days=1000)
                for route, times in routes.items():
                    transfer_time = timedelta(hours=0) if len(
                        common_lines) != 0 and route in common_lines else timedelta(hours=1)
                    if prev_line in common_lines and prev_line != route:
                        transfer_time += timedelta(hours=1)
                    for time_slot in times:
                        dep_time = convert_time(time_slot["dep_time"])
                        arr_time = convert_time(time_slot["arr_time"])

                        if dep_time > at_station_time:
                            time_btw_stops = arr_time - dep_time
                            waiting_time = dep_time - at_station_time

                            times_sum = time_btw_stops + waiting_time + transfer_time
                            if times_sum <= min_time:
                                min_time = times_sum
                                min_time_info = (times_sum.total_seconds() / 60,
                                                 time_slot["dep_time"], time_slot["arr_time"], route)
                return min_time_info

    def time_distance_between_stops(first_stop, second_stop):
        R = 6371.0
        MEAN_V = 20
        lat1, lon1 = graph_dict[first_stop]['coordinates']
        lat2, lon2 = graph_dict[second_stop]['coordinates']

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        time_distance = ((R * c) / MEAN_V) * 60  # (Odleglosc / srednia predkosc pojazdow) * 60 (minut)
        return time_distance

    path, route_info, cost = astar(graph_dict, start_stop, end_stop, time_distance_between_stops, time_at_station)

    path_with_info = []
    for i, stop in enumerate(path[:-1]):
        current_stop_info = route_info[i]
        path_with_info.append((stop,) + current_stop_info[1:])
    path_with_info.append(end_stop)
    end_time = time.time()
    return path_with_info, cost, end_time - start_time
