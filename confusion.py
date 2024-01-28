#confusion.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder

bus_route_data = pd.read_excel('bus_route_data.xlsx', parse_dates=['기준일'])
bus_route_data = bus_route_data[['기준일', '행정구명', 'ARS_ID', '정류소명', '노선수']]

bus_stop_location_data = pd.read_csv('updated_bus_stop_data.csv')
bus_stop_location_data = bus_stop_location_data[['ARS_ID', 'X좌표', 'Y좌표','Count']]

passenger_data = pd.read_csv('time_bus_people.csv', encoding='cp949')
time_columns = [f'{i}시승차총승객수' for i in range(24)] + [f'{i}시하차총승객수' for i in range(24)]
passenger_data = passenger_data[['버스정류장ARS번호'] + time_columns]

merged_data = pd.merge(passenger_data, bus_stop_location_data, how='left', left_on='버스정류장ARS번호', right_on='ARS_ID')
merged_data = pd.merge(merged_data, bus_route_data, how='left', left_on='버스정류장ARS번호', right_on='ARS_ID')

merged_data = merged_data[['X좌표', 'Y좌표','Count'] + time_columns + ['행정구명', '버스정류장ARS번호', '정류소명', '노선수']]

merged_data = merged_data.dropna()

label_encoder = LabelEncoder()
merged_data['행정구명'] = label_encoder.fit_transform(merged_data['행정구명'])

for i in range(24):
    merged_data[f'{i}시총승객수'] = merged_data[f'{i}시승차총승객수'] + merged_data[f'{i}시하차총승객수']

merged_data = merged_data.groupby(['X좌표', 'Y좌표', '행정구명', '정류소명', '노선수', 'Count']).sum().reset_index()

complexity_data = merged_data.groupby('정류소명').agg({
    **{f'{i}시총승객수': 'sum' for i in range(24)},  
    '노선수': 'max',  
    'X좌표': 'first',  
    'Y좌표': 'first',  
    'Count' : 'first',
}).reset_index()
max_passenger = complexity_data[[f'{i}시총승객수' for i in range(24)]].max().max()
max_route = complexity_data['노선수'].max()
max_count = complexity_data['Count'].max()

complexity_data[[f'{i}시총승객수' for i in range(24)]] = complexity_data[[f'{i}시총승객수' for i in range(24)]] / max_passenger
complexity_data['노선수'] = complexity_data['노선수'] / max_route
complexity_data['Count'] = 1 - complexity_data['Count'] / max_count  # Adjusting Count: higher values imply lower complexity

complexity_data['정류장복잡도'] = complexity_data[[f'{i}시총승객수' for i in range(24)] + ['노선수']].mean(axis=1)

sorted_complexity_data = complexity_data.sort_values(by='정류장복잡도', ascending=False)
top_100_complexity_data = sorted_complexity_data.head(100)


print(top_100_complexity_data[['정류소명', 'X좌표', 'Y좌표', '정류장복잡도']])
top_100_complexity_data[['정류소명', 'X좌표', 'Y좌표', '정류장복잡도']].to_csv('top_100_complexity_data.csv', index=False, encoding='cp949')

def get_complexity_by_stop_name(stop_name): 

    selected_row = sorted_complexity_data[sorted_complexity_data['정류소명'] == stop_name]
    if not selected_row.empty:
        complexity_info = selected_row[['정류소명','X좌표', 'Y좌표', '정류장복잡도']]
        print(complexity_info)
    else:
        print(f"정류소명 {stop_name}에 해당하는 정류장이 top 100 데이터에 없습니다.")