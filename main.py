import requests
import csv
from io import StringIO
import sys
from typing import Dict, List


class BestTowerFinder:
    def __init__(self, url: str):
        self.URL = url

    def get_data(self) -> Dict:
        """
        Fetches the list of file links from URL
        :returns: Dict : a dictionary of the JSON response
        """
        response = requests.get(self.URL)
        if response.status_code != 200:
            raise requests.exceptions.RequestException("Failed to retrieve data")

        return response.json()

    @staticmethod
    def get_entries(data: Dict, farm_id: str) -> Dict[str, List[int]]:
        """
        Fetches the CSV data from each link and filters entries based on farm_id
        :param data : Dict : the JSON response from get_data()
        :param farm_id : str : the farm_id to filter entries
        :returns : Dict[str, List[int]] : a dictionary of tower_id and their corresponding rssi values
        """
        entries = {}
        for link in data:
            try:
                csv_response = requests.get(link)
            except requests.exceptions.RequestException as e:
                print(f"Warning: Failed to retrieve CSV data from {link}: {e}")
                continue

            csv_content = StringIO(csv_response.text)
            csv_reader = csv.reader(csv_content)
            next(csv_reader)

            for row in csv_reader:
                if len(row) != 3:
                    print(f"Warning: detected a bad row: {row} from {link}")
                    continue
                current_farm_id = row[0]
                if current_farm_id == farm_id:
                    tower_id = row[1]
                    rssi = int(row[2])
                    if tower_id not in entries:
                        entries[tower_id] = []
                    entries[tower_id].append(rssi)

        return entries

    @staticmethod
    def get_best_tower(entries: Dict[str, List[float]]) -> str:
        """
        Averages the RSSI values for each tower_id and finds the highest rssi value.
        :param entries : Dict[str, List[int]]
        :returns: the best tower id : str
        """
        averages = {}
        for tower_id, rssi_values in entries.items():
            averages[tower_id] = sum(rssi_values) / len(rssi_values)

        max_average_rssi = float("-inf")
        max_tower_id = ""

        for tower_id, average_rssi in averages.items():
            if average_rssi > max_average_rssi:
                max_average_rssi = average_rssi
                max_tower_id = tower_id

        return max_tower_id

    def best_tower(self, farm_id: str) -> str:
        """
        Calls the other functions to find the best tower
        :param farm_id : str
        :returns: the id of the best tower
        """
        data = self.get_data()
        entries = self.get_entries(data, farm_id)

        return self.get_best_tower(entries)


def main():
    """
    If command line arguments are provided, they are treated as farm_ids and the best tower for each is printed.
    If no command line arguments are provided, a set of test case farm_ids are used instead.
    """
    best_tower_finder = BestTowerFinder("https://api.onizmx.com/lambda/tower_stream")

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            print(f"the best tower for {sys.argv[i]} is {best_tower_finder.best_tower(sys.argv[i])}")
    else:
        examples = [
            "419adc09-dbbe-49fd-9c1a-c807e37b3d4f",
            "06fc1b97-d26a-4081-b527-50184c387d89",
            "0fe4ff44-9fbb-4c4a-9395-35eab23b2a97",
            "48d3e41b-0a06-46c1-bf3c-91af704a3776",
            "29cb3049-3eb6-4bc9-b9f2-ba1e1718a901"
        ]
        print("No custom input prompt - running examples")

        for example in examples:
            print(f"the best tower for {example} is {best_tower_finder.best_tower(example)}")


if __name__ == '__main__':
    main()
