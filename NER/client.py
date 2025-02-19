import csv
import requests
import json
import time

#OUTPUT = "results_low.json"
#OUTPUT = "results_high.json"
#OUTPUT = "results_err3.json"
#OUTPUT = "results_err4.json"
#OUTPUT = "results_err5.json"
#OUTPUT = "results_err6.json"
#OUTPUT = "results_err7.json"
OUTPUT = "results_err8.json"

def read_strategy_file(file_path):
    """Leggi il file delle strategie e restituisci un dizionario."""
    strategy_map = {}
    try:
        with open(file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                time_slot = row["time_slot"]
                strategy = row["strategy"]
                strategy_map[time_slot] = strategy
    except Exception as e:
        print(f"Errore durante la lettura del file delle strategie: {e}")
    return strategy_map

def send_requests(strategy, carbon, num_requests):
    results = []
    for _ in range(num_requests):
        try:
            response = requests.get("http://127.0.0.1:50000/ans", params={"force": strategy})
            if response.status_code == 200:
                result = response.json()
                result["carbon"] = carbon
                results.append(result)
            else:
                results.append({"error": response.status_code, "carbon": carbon})
        except Exception as e:
            results.append({"error": str(e), "carbon": carbon})
        time.sleep(0.1)
    return results

def main():
    final_results = []
    #strategy_map = read_strategy_file("results_bis/error_3.csv")
    #strategy_map = read_strategy_file("results_bis/error_4.csv")
    #strategy_map = read_strategy_file("results_bis/error_5.csv")
    #strategy_map = read_strategy_file("results_bis/error_6.csv")
    #strategy_map = read_strategy_file("results_bis/error_7.csv")
    strategy_map = read_strategy_file("results_bis/error_8.csv")
    try:
        #with open("time_slots.csv", "r") as csv_file:
        with open("time_slots_bis.csv", "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                time_slot = row["time"]
                carbon = float(row["actual_carbon"])
                num_requests = int(row["actual_reqs"])
                #strategy = "LowPower"
                #strategy = "HighPower"
                strategy = strategy_map.get(time_slot)

                print(f"Processing: Strategy={strategy}, Carbon={carbon}, Requests={num_requests}")

                results = send_requests(strategy, carbon, num_requests)
                final_results.extend(results)
    except Exception as e:
        print(f"Errore durante la lettura del file CSV o l'elaborazione: {e}")
        return

    try:
        with open(OUTPUT, "w") as json_file:
            json.dump(final_results, json_file, indent=4)
        print(f"Risultati salvati in {OUTPUT}")
    except Exception as e:
        print(f"Errore durante il salvataggio dei risultati: {e}")

if __name__ == "__main__":
    main()