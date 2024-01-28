#300m_recommand.py
import pandas as pd
from math import radians, sin, cos, sqrt
bdf = pd.read_csv('bus_boarding_station.csv', parse_dates=['사용일자'],encoding='cp949', low_memory=False)

def find_routes_by_ars_number(ars_number):
    selected_rows = bdf[bdf['버스정류장ARS번호'] == ars_number]
    print(selected_rows)
    if not selected_rows.empty:

        unique_routes = selected_rows[['노선번호', '노선명']].drop_duplicates()
        print("\n이 정류장에 지나가는 노선 정보:")
        print(unique_routes)
    else:
        print(f"ARS 번호 {ars_number}에 해당하는 정류장이 데이터에 없습니다.")

def haversine(lon1, lat1, lon2, lat2):
    
    R = 6371.0  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * sqrt(a)

    distance = R * c * 1000  
    return distance

def find_nearby_stations(target_station, all_stations, radius=300.0):

    nearby_stations = []

    target_lat, target_lon = target_station['X좌표'], target_station['Y좌표']

    for index, station in all_stations.iterrows():
        distance = haversine(target_lon, target_lat,
                             station['Y좌표'], station['X좌표'])

        if distance <= radius:
            if station['정류소명'] != target_station['정류소명']:
                nearby_stations.append(station['ARS_ID'])

    return nearby_stations

df = pd.read_csv('seoul_map_data.csv',  low_memory=False)
df = df.drop_duplicates(subset='ARS_ID')

target_station_ARS = "22020"
target_station = df[df['ARS_ID'] == int(target_station_ARS)]

if not target_station.empty:
    target_station = target_station.iloc[0]  # 첫 번째 행 선택
    nearby_stations = find_nearby_stations(target_station, df, 300)

    # 결과 출력
    print(f"\n반경 300m 내의 정류장:")
    for station_ARS in nearby_stations:
        # print(station_ARS)
        print(df[df['ARS_ID'] == int(station_ARS)])
    print("해당 정류장을 지나가는 노선")
    find_routes_by_ars_number(str(target_station_ARS))