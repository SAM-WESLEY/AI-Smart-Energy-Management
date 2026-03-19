import numpy as np, pickle, os, random
from sklearn.ensemble import IsolationForest, RandomForestRegressor

MODEL = 'models/energy_model.pkl'

class MLPredictor:
    def __init__(self):
        self.model = None
        self.iforest = IsolationForest(contamination=0.1, random_state=42)
        self.history_data = []
        if os.path.exists(MODEL):
            try: self.model = pickle.load(open(MODEL,'rb'))
            except: pass

    def predict(self, history):
        if not history: return {"predicted_kwh":0.0,"anomaly":False}
        powers = [h["power"] for h in history[-20:]]
        self.history_data.append(powers[-1])
        anomaly = False
        if len(self.history_data) >= 10:
            X = np.array(self.history_data[-20:]).reshape(-1,1)
            self.iforest.fit(X)
            pred = self.iforest.predict([[powers[-1]]])
            anomaly = pred[0] == -1
        avg = np.mean(powers) if powers else 0
        predicted = round(avg * 24 / 1000, 3)
        return {"predicted_kwh": predicted, "anomaly": bool(anomaly)}
