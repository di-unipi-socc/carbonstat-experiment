import subprocess
import csv
from datetime import datetime

programs = ["low.py", "medium.py", "high.py"]
input_file = "data/input.txt"
output_file = "execution_times.csv"
results = []

for program in programs:
    for test_num in range(10):
        try:
            start = datetime.now()
            subprocess.run(["python3", program, input_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            end = datetime.now()
            elapsed = round(end.timestamp() - start.timestamp(),3)
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'esecuzione di {program} numero {test_num + 1}: {e}")
            continue
        results.append({"Program": program,"ExecutionTime": elapsed,"TestNum": test_num + 1})
        print(f"Terminata esecuzione di {program} numero {test_num + 1}")

with open(output_file, mode="w", newline="") as csv_file:
    fieldnames = ["Program", "ExecutionTime", "TestNum"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)