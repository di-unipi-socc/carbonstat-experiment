from datetime import datetime
from enum import Enum
from flask import Flask,request,jsonify
from os import environ
from math import floor

# ------ STRATEGIES ------
from flavours.interface import CarbonAwareStrategy
from flavours.low_power import LowPowerStrategy
from flavours.medium_power import MediumPowerStrategy
from flavours.high_power import HighPowerStrategy

class CarbonAwareStrategies(Enum):
    LowPower = LowPowerStrategy
    MediumPower = MediumPowerStrategy
    HighPower = HighPowerStrategy

# ------ CONTEXT ------
class Context:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
    def __init__(self):
        self.assignment = {}
        assignment = open("simulation/results/error_7.csv")
        for a_line in list(assignment)[1:]:
            a = a_line.replace("\n","").split(",")
            timestamp = datetime.strptime(a[0],"%Y-%m-%dT%H:%MZ")
            strategy = a[1]
            self.assignment[timestamp.hour + 0.5*floor(timestamp.minute/30)] = CarbonAwareStrategies[strategy].value
        assignment.close()
    
    def getCarbonAwareStrategy(self,force_strategy) -> CarbonAwareStrategy:
        if force_strategy is not None:
            return CarbonAwareStrategies[force_strategy].value
        now = datetime.now()
        return self.assignment[now.hour + 0.5*floor(now.minute/30)]

# ------ SERVICE ------
app = Flask(__name__)

with open("data/input.txt","r") as text:
    app.data = text.read()
app.context = Context()

@app.route("/")
def nop():
    force_strategy = request.args.get("force")
    strategy = app.context.getCarbonAwareStrategy(force_strategy)
    answer = strategy.nop() + "\n"
    return answer

@app.route("/ans")
def ans():
    force_strategy = request.args.get("force")
    strategy = app.context.getCarbonAwareStrategy(force_strategy)
    start = datetime.now()
    ans = strategy.ans(app.data)
    end = datetime.now()
    elapsed = round(end.timestamp() - start.timestamp(),3)
    result = {}
    result["answer"] = ans
    result["time"] = elapsed
    result["strategy"] = strategy.nop()
    return jsonify(result)

app.run(host='0.0.0.0',port=50000)