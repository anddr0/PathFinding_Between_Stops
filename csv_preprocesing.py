import pandas as pd
import json


#   ----------------------------CSV TO GRAPH----------------------------
class Graph:
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path)
        self.graph_dict = {}

        for index, row in df.iterrows():
            line = row['line']
            start_stop = row['start_stop']
            end_stop = row['end_stop']

            start_stop_coordinates = (row['start_stop_lat'], row['start_stop_lon'])
            end_stop_coordinates = (row['end_stop_lat'], row['end_stop_lon'])

            connection = {'dep_time': row['departure_time'], 'arr_time': row['arrival_time']}

            if start_stop not in self.graph_dict:
                self.graph_dict[start_stop] = {'end_stops': {}, 'coordinates': start_stop_coordinates}

            if end_stop not in self.graph_dict[start_stop]['end_stops']:
                self.graph_dict[start_stop]['end_stops'][end_stop] = {}

            if line not in self.graph_dict[start_stop]['end_stops'][end_stop]:
                self.graph_dict[start_stop]['end_stops'][end_stop][line] = []

            self.graph_dict[start_stop]['end_stops'][end_stop][line].append(connection)

graph = Graph("connection_graph.csv")
with open('stops_graph.json', 'w', encoding='utf-8') as json_file:
    json.dump(graph.graph_dict, json_file, indent=4, ensure_ascii=False)


#   --------------------------------------------------------------------


