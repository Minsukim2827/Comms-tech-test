# Comms-tech-test

# Best Tower Finder

This is a Python script that finds the best tower for a given farm id. The best tower is determined based on the highest average RSSI.

## Getting Started

To get a copy of this project up and running on your local machine, follow these steps:

1. Ensure you have Python (python3) installed on your system.
2. install requests: This library is used for making HTTP requests to fetch data from the given URL.
```bash
pip install requests
```
4. Clone the GitHub repository containing the code.
```bash
git clone https://github.com/Minsukim2827/Comms-tech-test.git
```
6. Open a terminal and navigate to the directory where the code is located.
7. Run the program with the following command:
```bash
python3 main.py <farm_id1> <farm_id2> ...
```
Replace <farm_id1>, <farm_id2>, etc., with the farm IDs you want to test. If no farm IDs are provided, the program will run with a set of example farm IDs.

## Example
```bash
python3 main.py f10e802c-55a3-4407-ab6e-16cefa5fd2cc 48d3e41b-0a06-46c1-bf3c-91af704a3776 0b515fbb-2981-4f99-9141-dce1c46beb6f
```

or you can also just run the file itself, if no farm IDs are provided, the program will run with a set of example test cases
```bash
python3 main.py 
```

## Problems i Found while debugging

When reading the rows of some of the CSV files, i encounted some problems:

![image](https://github.com/Minsukim2827/Comms-tech-test/assets/122320786/a1e1fcb0-6cb9-4391-b548-d214f56028be)
![image](https://github.com/Minsukim2827/Comms-tech-test/assets/122320786/e1971cef-53cd-4abb-a7f1-effe313be9b9)

It appears that I do not have the correct permissions when accessing 2 specific files in the API, when accessing these CSV file links, I see something like this:

![image](https://github.com/Minsukim2827/Comms-tech-test/assets/122320786/1cfbb9b5-cf19-43e2-82de-2b21afa6bfb4)


