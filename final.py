#final.py
import pandas as pd
from sklearn.cluster import KMeans

def rank_stations(station_data, k=5):
    features = ['이동거리', '이동시간', '혼잡도']

    X = station_data[features]

    kmeans = KMeans(n_clusters=k, random_state=42)
    station_data['Cluster'] = kmeans.fit_predict(X)

    cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=features)
    ranked_stations = pd.DataFrame()

    for cluster_index in range(k):
        cluster_data = station_data[station_data['Cluster'] == cluster_index]
        
        cluster_data['Distance'] = ((cluster_data[features] - cluster_centers.iloc[cluster_index])**2).sum(axis=1)**0.5

        cluster_data = cluster_data.sort_values(by='Distance')
        cluster_data['Rank'] = range(1, len(cluster_data) + 1)

        ranked_stations = pd.concat([ranked_stations, cluster_data])

    ranked_stations = ranked_stations[['정류장명', 'Rank', '이동거리', '이동시간', '혼잡도']]
    ranked_stations = ranked_stations.sort_values(by='Rank')

    return ranked_stations

station_data = pd.DataFrame({
    '정류장명': ["센트럴시티", "서울성모병원", "고속터미널호남선", "호남고속터미널", "경부고속터미널","한신2차정문","호남고속.신세계"],
    '이동거리': [2053, 3423, 4018, 4017, 3993,2591,1533],
    '이동시간': [288, 475, 520, 520, 505,532,214],
    '혼잡도': [0.00297, 0.004979, 0.010115, 0.005101, 0.001321,0.000989,0.0074]
})
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualize_clusters(station_data, k=3):
    features = ['이동거리', '이동시간', '혼잡도']

    X = station_data[features]

    kmeans = KMeans(n_clusters=k, random_state=42)
    station_data['Cluster'] = kmeans.fit_predict(X)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    for cluster_index in range(k):
        cluster_data = station_data[station_data['Cluster'] == cluster_index]
        ax.scatter(cluster_data[features[0]], cluster_data[features[1]], cluster_data[features[2]], label=f'Cluster {cluster_index + 1}')

    ax.set_xlabel(features[0])
    ax.set_ylabel(features[1])
    ax.set_zlabel(features[2])
    ax.set_title('K-Means Clustering')

    plt.legend()
    plt.show()

visualize_clusters(station_data, k=3)

ranked_stations = rank_stations(station_data, k=3)
print(ranked_stations)