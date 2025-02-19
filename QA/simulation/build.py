import pandas as pd
df = pd.read_csv("execution_times.csv")
average = df.groupby("Program")["ExecutionTime"].mean().reset_index()
average.columns = ["strategy", "elapsed_time"]
map = {"low.py": "LowPower", "medium.py": "MediumPower", "high.py": "HighPower"}
average["strategy"] = average["strategy"].map(map)
average["error"] = [6.85, 13, 8.2]
average.to_csv("strategies.csv", index=False)