HIGH_POWER = 4000
LOW_POWER  = 500

class LoadController:
    def decide(self, data):
        power = data.get("power", 0) if isinstance(data, dict) else 0
        if power > HIGH_POWER: return "REDUCED"
        if power < LOW_POWER:  return "STANDBY"
        return "ON"
