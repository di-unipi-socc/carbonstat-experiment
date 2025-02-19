from datetime import datetime
from enum import Enum
from flask import Flask,request,jsonify
from os import environ
from math import floor

# ------ STRATEGIES ------
# Import and enum carbon-aware strategies (aka. flavours)
from flavours.interface import CarbonAwareStrategy
from flavours.low_power import LowPowerStrategy
from flavours.medium_power import MediumPowerStrategy

class CarbonAwareStrategies(Enum):
    LowPower = LowPowerStrategy
    MediumPower = MediumPowerStrategy

# ------ CONTEXT ------
# Carbon-aware context
class Context:
    # constructor
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
    # initializer
    def __init__(self):
        self.assignment = {}
        assignment = open("simulation/results/error_15.csv")
        for a_line in list(assignment)[1:]:
            a = a_line.replace("\n","").split(",")
            timestamp = datetime.strptime(a[0],"%Y-%m-%dT%H:%MZ")
            strategy = a[1]
            self.assignment[timestamp.hour + 0.5*floor(timestamp.minute/30)] = CarbonAwareStrategies[strategy].value
        assignment.close()
    
    # getter for carbon-aware strategy
    def getCarbonAwareStrategy(self,force_strategy) -> CarbonAwareStrategy:
        if force_strategy is not None:
            return CarbonAwareStrategies[force_strategy].value
        now = datetime.now()
        return self.assignment[now.hour + 0.5*floor(now.minute/30)]

# ------ SERVICE ------
app = Flask(__name__)

# app data
with open("data/input.txt","r") as text:
    app.data = text.read()

# set service's context
app.context = Context()

@app.route("/")
def nop():
    # Parse params and check if forced to run a given strategy
    force_strategy = request.args.get("force")
    # Get carbon-aware strategy
    strategy = app.context.getCarbonAwareStrategy(force_strategy)
    # Invoke strategy with dynamic typing
    answer = strategy.nop() + "\n"
    return answer

@app.route("/ans")
def ans():
    # Parse params and check if forced to run a given strategy
    force_strategy = request.args.get("force")
    # Get carbon-aware strategy
    strategy = app.context.getCarbonAwareStrategy(force_strategy)
    # Invoke strategy with dynamic typing (and measure running time)
    start = datetime.now()
    ans = strategy.ans(app.data)
    end = datetime.now()
    elapsed = round(end.timestamp() - start.timestamp(),3)
    # Return result and elapsed time
    result = {}
    result["answer"] = ans
    result["time"] = elapsed
    result["strategy"] = strategy.nop()
    return jsonify(result)

app.run(host='0.0.0.0',port=50000)