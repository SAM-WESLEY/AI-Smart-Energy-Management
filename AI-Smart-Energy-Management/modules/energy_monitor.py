import time, math, json, os

class EnergyMonitor:
    def __init__(self):
        self.demo = True
        self._connect()

    def _connect(self):
        if not os.path.exists('config.json'): return
        try:
            cfg = json.load(open('config.json')).get('mqtt',{})
            if not cfg.get('enabled'): return
            import paho.mqtt.client as mqtt
            c = mqtt.Client()
            c.connect(cfg['broker'], cfg.get('port',1883))
            c.subscribe(cfg.get('topic','energy/readings'))
            c.loop_start()
            self.demo = False
        except Exception as e: print(f"[EnergyMonitor] {e}")

    def get_readings(self):
        t  = time.time()
        v  = round(220 + 5*math.sin(t/10), 1)
        i  = round(2.5 + 1.5*abs(math.sin(t/7)), 2)
        pf = round(0.88 + 0.05*math.sin(t/15), 2)
        p  = round(v*i*pf, 1)
        kwh = round((p/1000)*(t%3600)/3600, 4)
        return {"voltage":v,"current":i,"power":p,"power_factor":pf,
                "energy_kwh":kwh,"frequency":round(50+0.1*math.sin(t/20),1)}
