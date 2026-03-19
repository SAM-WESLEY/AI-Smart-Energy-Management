from flask import Flask, render_template, jsonify
import threading, time, random, math
from modules.energy_monitor  import EnergyMonitor
from modules.ml_predictor    import MLPredictor
from modules.load_controller import LoadController
from modules.alert_system    import AlertSystem

app        = Flask(__name__)
monitor    = EnergyMonitor()
predictor  = MLPredictor()
controller = LoadController()
alerter    = AlertSystem()

TARIFF = 6.5  # Rs per kWh

state = {
    "voltage":0.0,"current":0.0,"power":0.0,"power_factor":0.0,
    "energy_kwh":0.0,"frequency":50.0,"cost":0.0,"anomaly":False,
    "predicted_kwh":0.0,"load_status":"ON","alert_count":0,
    "last_updated":"—","history":[],
}

def monitor_loop():
    while True:
        try:
            data = monitor.get_readings()
            if data:
                state.update({k: data[k] for k in data})
                state["cost"] = round(data["energy_kwh"] * TARIFF, 2)
                state["last_updated"] = time.strftime("%H:%M:%S")
                r = predictor.predict(state["history"])
                state["predicted_kwh"] = r["predicted_kwh"]
                state["anomaly"] = r["anomaly"]
                state["load_status"] = controller.decide(data)
                state["history"].append({"time": state["last_updated"],
                    "power": data["power"], "voltage": data["voltage"],
                    "current": data["current"], "kwh": data["energy_kwh"],
                    "anomaly": r["anomaly"]})
                if len(state["history"]) > 50: state["history"].pop(0)
                if r["anomaly"] or data["power"] > 5000:
                    alerter.send_alert(state); state["alert_count"] += 1
        except Exception as e: print(f"[Monitor] {e}")
        time.sleep(5)

@app.route('/') 
def index(): return render_template('index.html')

@app.route('/status')
def status(): return jsonify(state)

@app.route('/history')
def history(): return jsonify(state["history"])

@app.route('/simulate')
def simulate():
    t = time.time()
    v = round(220 + 5*math.sin(t/10), 1)
    i = round(random.uniform(0.5, 8.0), 2)
    p = round(v * i * random.uniform(0.8, 1.0), 1)
    pf = round(random.uniform(0.80, 0.99), 2)
    kwh = round(state["energy_kwh"] + p/3600000*5, 4)
    f = round(50 + random.uniform(-0.2, 0.2), 1)
    state.update({"voltage":v,"current":i,"power":p,"power_factor":pf,
        "energy_kwh":kwh,"frequency":f,"cost":round(kwh*TARIFF,2),
        "last_updated":time.strftime("%H:%M:%S")})
    r = predictor.predict(state["history"])
    state["predicted_kwh"] = r["predicted_kwh"]
    state["anomaly"] = r["anomaly"]
    state["load_status"] = controller.decide(state)
    state["history"].append({"time":state["last_updated"],"power":p,
        "voltage":v,"current":i,"kwh":kwh,"anomaly":r["anomaly"]})
    if len(state["history"]) > 50: state["history"].pop(0)
    return jsonify({"status":"simulated","data":state})

if __name__ == '__main__':
    threading.Thread(target=monitor_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
