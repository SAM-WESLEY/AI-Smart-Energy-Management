import smtplib, json, os
from datetime import datetime
from email.mime.text import MIMEText

class AlertSystem:
    def __init__(self):
        self.cfg = {}
        self.last = 0
        if os.path.exists('config.json'):
            try: self.cfg = json.load(open('config.json'))
            except: pass

    def send_alert(self, state):
        import time
        if time.time() - self.last < 300: return
        self.last = time.time()
        msg = f"ENERGY ALERT\nPower: {state['power']}W\nAnomaly: {state['anomaly']}\nTime: {datetime.now()}"
        print(f"[AlertSystem] {msg}")
        ecfg = self.cfg.get('email',{})
        if ecfg.get('enabled'):
            try:
                m = MIMEText(msg)
                m['Subject']='⚡ Energy Alert'; m['From']=ecfg['sender']; m['To']=ecfg['recipient']
                with smtplib.SMTP_SSL('smtp.gmail.com',465) as s:
                    s.login(ecfg['sender'],ecfg['password']); s.send_message(m)
            except Exception as e: print(f"[AlertSystem] {e}")
