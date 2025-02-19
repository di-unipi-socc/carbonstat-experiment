import json
import csv

def calculate_error(strategy):
    errors = {
        "LOW_POWER": 8.3,
        "HIGH_POWER": 2.5
    }
    return errors.get(strategy, 0.0)

def process_json_to_csv(json_files, output_csv):
    results = []

    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            if data:
                strategy = data[0]['strategy']
                total_time = sum(item['time'] for item in data)
                elapsed_time = total_time / len(data) if len(data) > 0 else 0
                error = calculate_error(strategy)
                results.append({
                    'strategy': strategy.replace('_', ''),
                    'elapsed_time': elapsed_time,
                    'error': error
                })

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['strategy', 'elapsed_time', 'error']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

json_files = ['results_high.json', 'results_low.json']
output_csv = 'strategies.csv'
process_json_to_csv(json_files, output_csv)