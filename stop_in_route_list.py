#stop_in_route_list.py
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('bus_boarding_station.csv', parse_dates=['사용일자'],encoding='cp949', low_memory=False)

def find_routes_by_ars_number(ars_number):
    # 입력된 ARS 번호에 해당하는 행 선택
    selected_rows = df[df['버스정류장ARS번호'] == ars_number]
    if not selected_rows.empty:
        # ARS 번호에 해당하는 정류장 정보 출력
        # 정류장에 지나가는 노선 정보 출력
        unique_routes = selected_rows[['노선번호']].drop_duplicates()
        routes_dict = unique_routes.to_dict()
        print("\n이 정류장에 지나가는 노선 정보:")
        print(routes_dict["노선번호"].values())
    else:
        print(f"ARS 번호 {ars_number}에 해당하는 정류장이 데이터에 없습니다.")

user_ars_number = input("ARS 번호를 입력하세요: ")
find_routes_by_ars_number(user_ars_number)