import json
import os
import csv
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-darkgrid')

error_mapping = {
    "LOW_POWER": 8.3,
    "HIGH_POWER": 2.5
}

file_list = [
    "results/results_low.json",
    "results/results_high.json",    
    #"results_bis/results_low.json",
    #"results_bis/results_high.json",    
]

for num in range(3, 9):
    file_list.append(f"results/results_err{num}.json")
    #file_list.append(f"results_bis/results_err{num}.json")

labels = []
avg_errors = []
total_carbons = []
csv_data = []

for filename in file_list:
    with open(filename, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Errore nel file {filename}: {e}")
            continue

    sum_errors = 0.0
    total_objects = 0
    total_carbon = 0.0

    for item in data:
        strategy = item.get("strategy")
        time = item.get("time", 0)
        intensity = item.get("carbon", 0)
        total_objects += 1
        sum_errors += error_mapping[strategy]
        total_carbon += 0.05 * (time / 3600) * intensity

    if total_objects > 0:
        avg_error = sum_errors / total_objects
    else:
        avg_error = 0

    label = os.path.basename(filename)[len("results_"):-len(".json")]

    labels.append(label)
    avg_errors.append(avg_error)
    total_carbons.append(total_carbon)
    csv_data.append([label, round(avg_error, 2), round(total_carbon, 2)])
    
    print(f"File: {filename}")
    print(f"  Errore medio: {avg_error:.2f}")
    print(f"  Carbonio totale: {total_carbon:.2f} gCO2-eq")
    print("")

csv_filename = "graph.csv"
#csv_filename = "graph_bis.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["file", "error", "carbon"])
    writer.writerows(csv_data)

plt.figure(figsize=(16, 12))
plt.scatter(total_carbons, avg_errors, color='blue', s=150, marker='o', edgecolor='k', alpha=0.8)

for i, label in enumerate(labels):
    plt.annotate(label, (total_carbons[i], avg_errors[i]),
                 textcoords="offset points", xytext=(5,5), ha='left', fontsize=20,
                 bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))

plt.xlabel("Carbonio totale (gCO₂-eq)", fontsize=24, fontweight='bold')
plt.ylabel("Errore medio", fontsize=24, fontweight='bold')
plt.title("NER", fontsize=28, fontweight='bold')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True)
plt.tight_layout()
plt.savefig("graph.png", dpi=300)
#plt.savefig("graph_bis.png", dpi=300)