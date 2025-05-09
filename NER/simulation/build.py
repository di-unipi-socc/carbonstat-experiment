import pandas as pd
df = pd.read_csv("execution_times.csv")
average = df.groupby("Program")["ExecutionTime"].mean().reset_index()
average.columns = ["strategy", "elapsed_time"]
map = {"low.py": "LowPower", "medium.py": "MediumPower", "high.py": "HighPower"}
average["strategy"] = average["strategy"].map(map)
average["error"] = [2.5, 8.7, 8.3]
average.to_csv("strategies.csv", index=False)