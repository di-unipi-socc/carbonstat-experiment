import pandas as pd
file_range = range(3, 9)
stats = []

for file_number in enumerate(file_range):
    file_name = f"error_{file_number}.csv"
    df = pd.read_csv(file_name)
    low_count = df["strategy"].str.count("LowPower").sum()
    medium_count = df["strategy"].str.count("MediumPower").sum()
    high_count = df["strategy"].str.count("HighPower").sum()
    stats.append({"error": file_number, "low": low_count, "medium": medium_count, "high": high_count})

results = pd.DataFrame(stats)
results.to_csv("stats.csv", index=False)