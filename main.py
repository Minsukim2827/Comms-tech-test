import requests
import csv
from io import StringIO


def get_data():
    response = requests.get("https://api.onizmx.com/lambda/tower_stream")
    # raise an exception if fetching http link is unsuccessful
    if response.status_code != 200:
        raise Exception("failed to retrieve data")

    return response.json()


def get_entries(data, farm_id):
    entries = {}
    for link in data:
        try:
            csv_response = requests.get(link)
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to retrieve CSV data from {link}: {e}")
            continue  # skip this link and move on to the next one

        csv_content = StringIO(csv_response.text)
        csv_reader = csv.reader(csv_content)
        next(csv_reader)  # skip 1st line as it's the data format

        for row in csv_reader:
            current_farm_id = row[0]
            if current_farm_id == farm_id:
                tower_id = row[1]
                rssi = int(row[2])
                if tower_id not in entries:
                    entries[tower_id] = []
                entries[tower_id].append(rssi)

    return entries


def get_best_tower(entries):
    for towerId, rssiValues in entries.items():
        entries[towerId] = sum(rssiValues) / len(rssiValues)  # average the RSSI values for each towerId

    max_average_rssi = float("-inf")
    max_tower_id = ""

    for towerId, averageRSSI in entries.items():  # find the towerId with the highest averageRSSI value
        if averageRSSI > max_average_rssi:
            max_average_rssi = averageRSSI
            max_tower_id = towerId

    return max_tower_id


def best_tower(farm_id):  # this function calls the other functions to find the best tower
    data = get_data()
    entries = get_entries(data, farm_id)

    return get_best_tower(entries)


if __name__ == '__main__':

    print(best_tower("419adc09-dbbe-49fd-9c1a-c807e37b3d4f"))
    print(best_tower("06fc1b97-d26a-4081-b527-50184c387d89"))
    print(best_tower("0fe4ff44-9fbb-4c4a-9395-35eab23b2a97"))
    print(best_tower("48d3e41b-0a06-46c1-bf3c-91af704a3776"))
    print(best_tower("29cb3049-3eb6-4bc9-b9f2-ba1e1718a901"))
