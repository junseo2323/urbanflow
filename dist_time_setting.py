#dist_time_setting.py

import requests
import pandas as pd
import xml.etree.ElementTree as ET

def get_kakao_directions(api_key, origin, destination, waypoints):

    base_url = "https://apis-navi.kakaomobility.com/v1/waypoints/directions"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'KakaoAK {api_key}'}
    
    params = {
        "origin": {
         "x": str(origin[0]),
        "y": str(origin[1])
        },
        "destination": {
            "x": str(destination[0]),
            "y": str(destination[1])
        },
        "waypoints": [
            {
                "name": "name0",
                "x": str(waypoints[0]),
                "y": str(waypoints[1])
            }
        ],
        "priority": "RECOMMEND",
        "car_fuel": "GASOLINE",
        }

    response = requests.post(base_url, headers=headers, json=params)
    data = response.json()
    return data



bus_stop_location_data = pd.read_csv('seoul_map_data.csv', low_memory=False)

def get_coordinates_by_ars_id(ars_id, bus_stop_location_data):
    station_info = bus_stop_location_data[bus_stop_location_data['ARS_ID'] == int(ars_id)]

    if not station_info.empty:
        x_coordinate = station_info.iloc[0]['X좌표']
        y_coordinate = station_info.iloc[0]['Y좌표']
        return x_coordinate , y_coordinate
    else:
        return None
api_key = 'a6a5d124ef41b00d5b920fec22632217'
od_list = [[[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [127.0003902, 37.50694399]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0138855, 37.50491756], [126.9957194, 37.50341813]], [[127.0077586, 37.50920911], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0116013, 37.50279745], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [127.0003902, 37.50694399]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0077586, 37.50920911], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]], [[127.0116013, 37.50279745], [126.9957194, 37.50341813]], [[127.0118927, 37.50841143], [126.9957194, 37.50341813]]]
origin = (127.011892, 37.50841143) 
destination = (126.9957194, 37.50341813) 

ars_list = [22213,22215,22220,22505,22520,22843,22855]

res_list_distense = []
reS_list_time = []
for t in od_list:
    origin = t[0]
    destination = t[1]
    for ars in ars_list :
        ars = str(ars)
        coordinates = get_coordinates_by_ars_id(ars, bus_stop_location_data)

        if coordinates:
            x_coordinate, y_coordinate = coordinates
            waypoints = [x_coordinate, y_coordinate]

        directions = get_kakao_directions(api_key, origin, destination, waypoints)
        res_list_distense.append((directions['routes'][0])['summary']['distance'])
        reS_list_time.append((directions['routes'][0])['summary']['duration'])
bus_route_num_list = ['9408', '142', '640', '452', '4212', 'N75', '8641', '6411', '360', '401', '361', '148','9408', '540', '8541', '4318', '142', '143', '640', '452', '4212', '0411', 'N75', '8641', '6411', '643', '360', '401', '345', '361', '3420', '148']
stop_list = ["센트럴시티","서울성모병원","고속터미널호남선","호남고속터미널","경부고속터미널","한신2차정문","호남고속.신세계"]
for a in bus_route_num_list:
    for x in range(7):
        print(a,stop_list[x],res_list_distense[x],reS_list_time[x])