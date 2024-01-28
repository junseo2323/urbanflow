#route.py
import requests
import xml.etree.ElementTree as ET

api_key = "1Fw+4cm6AcORhPWwCdQZMLOA4k4VVMJ74PKhKrRnxQh1ChLnR7MZ34SjFE0+B1oDyXEy08HVIkJgN7Zhxzpmlw=="
bus_route_num_list = ['9408', '142', '640', '452', '4212', 'N75', '8641', '6411', '360', '401', '361', '148','9408', '540', '8541', '4318', '142', '143', '640', '452', '4212', '0411', 'N75', '8641', '6411', '643', '360', '401', '345', '361', '3420', '148']
base_url_1 = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList"
step_list = []
for bus_route_num in bus_route_num_list:
    params1 = {
        'serviceKey': api_key,
        'strSrch': bus_route_num,
    }

    input_station_ars = "22019"

    try:
        response1 = requests.get(base_url_1, params=params1)
        response1.raise_for_status()  

        root = ET.fromstring(response1.content)

        for item1 in root.findall('.//itemList'):
            route_name = item1.find('busRouteNm').text
            route_id = item1.find('busRouteId').text
            company_name = item1.find('corpNm').text
            start = item1.find('stStationNm').text
            end = item1.find('edStationNm').text

    except requests.exceptions.RequestException as e:
        print("API 호출에 실패했습니다.", e)
    except ET.ParseError as e:
        print("XML 파싱에 실패했습니다.", e)


    bus_route_id = route_id
    base_url_2 = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute"

    params2 = {
        'serviceKey': api_key,
        'busRouteId': bus_route_id,
    }

    try:
        response2 = requests.get(base_url_2, params=params2)
        response2.raise_for_status() 

        root = ET.fromstring(response2.content)

        for item2 in root.findall('.//itemList'):
            temp = []
            route_seq = item2.find('seq').text
            station_ars = item2.find('stationNo').text
            
            if input_station_ars == station_ars:
                seq_find = route_seq
                
                for item2 in root.findall('.//itemList'):
                    route_seq = item2.find('seq').text
                    station_ars = item2.find('stationNo').text


                    if int(route_seq) == int(seq_find) - 1:
                        print("[이전 정류장]")
                        temp.append(station_ars)
                        print(f"정류장ARS번호: {station_ars}")
                        
                    if int(route_seq) == int(seq_find) + 1:
                        print("[다음 정류장]")
                        temp.append(station_ars)
                        print(f"정류장ARS번호: {station_ars}")
            if temp:
                step_list.append(temp)
    
    except requests.exceptions.RequestException as e:
        print("API 호출에 실패했습니다.", e)
    except ET.ParseError as e:
        print("XML 파싱에 실패했습니다.", e)
    

print(step_list)