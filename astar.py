import heapq
import time
import math
from geopy import distance
from haversine import haversine
from datetime import timedelta
from funcs import convert_time


def go_astar(graph_dict, start_stop, end_stop, current_time):
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
                min_time, dep_time, arr_time, line = time_between_stops(current, neighbor, station_time)
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

    def time_distance_between_stops_geopy(start, end):
        MEAN_V = 20
        start_coordinate = graph_dict[start]['coordinates']
        end_coordinate = graph_dict[end]['coordinates']
        return (distance.distance(start_coordinate, end_coordinate).km / MEAN_V) * 60

    def time_distance_between_stops_haversine(start, end):
        MEAN_V = 20
        start_coordinate = graph_dict[start]['coordinates']
        end_coordinate = graph_dict[end]['coordinates']
        return (haversine(start_coordinate, end_coordinate).km / MEAN_V) * 60

    path, route_info, cost = astar(graph_dict, start_stop, end_stop, time_distance_between_stops_geopy, time_at_station)

    path_with_info = []
    for i, stop in enumerate(path[:-1]):
        current_stop_info = route_info[i]
        path_with_info.append((stop,) + current_stop_info[1:])
    path_with_info.append(end_stop)
    end_time = time.time()
    return path_with_info, cost, end_time - start_time

