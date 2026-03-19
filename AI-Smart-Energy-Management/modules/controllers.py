import json, os, smtplib, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

CONFIG_PATH = 'config.json'


# ── Load Controller ────────────────────────────────────────────────────────────
class LoadController:
    def __init__(self):
        self.relay_state = True
        self._init_gpio()

    def _init_gpio(self):
        try:
            import RPi.GPIO as GPIO
            self.gpio    = GPIO
            self.pin     = 17
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.HIGH)
            self.hw = True
            print("[LoadController] GPIO initialized on pin 17.")
        except Exception:
            self.hw = False
            print("[LoadController] No GPIO — relay control in demo mode.")

    def set_relay(self, on: bool):
        self.relay_state = on
        if self.hw:
            try:
                import RPi.GPIO as GPIO
                GPIO.output(self.pin, GPIO.HIGH if on else GPIO.LOW)
            except Exception as e:
                print(f"[LoadController] GPIO error: {e}")
        print(f"[LoadController] Relay {'ON' if on else 'OFF'}")

    def get_state(self):
        return self.relay_state


# ── Bill Calculator ────────────────────────────────────────────────────────────
class BillCalculator:
    # Indian electricity tariff (₹ per kWh, tiered)
    TARIFF = [
        (0,   100,  3.50),
        (100, 200,  4.50),
        (200, 500,  6.00),
        (500, 1e9,  7.50),
    ]

    def calculate(self, energy_kwh):
        cost = 0.0
        remaining = energy_kwh
        for low, high, rate in self.TARIFF:
            slab = min(remaining, high - low)
            if slab <= 0:
                break
            cost      += slab * rate
            remaining -= slab

        days_elapsed = max(1, datetime.now().day)
        monthly_est  = cost / days_elapsed * 30

        return {
            "today":       round(cost, 2),
            "month":       round(monthly_est, 2),
            "tariff_rate": self._current_rate(energy_kwh),
        }

    def _current_rate(self, kwh):
        for low, high, rate in self.TARIFF:
            if low <= kwh < high:
                return rate
        return self.TARIFF[-1][2]


# ── Alert System ───────────────────────────────────────────────────────────────
class AlertSystem:
    COOLDOWN = 300

    def __init__(self):
        self.last_alert = 0
        self.cfg        = {}
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH) as f:
                    self.cfg = json.load(f)
            except Exception:
                pass

    def send_alert(self, state):
        now = time.time()
        if now - self.last_alert < self.COOLDOWN:
            return
        self.last_alert = now
        subject = f"⚡ ENERGY ALERT — {state['alert_level']}"
        body    = self._compose(state)
        self._email(subject, body)
        self._sms(body[:160])

    def _compose(self, s):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
SMART ENERGY ALERT
{'='*40}
Time         : {ts}
Alert Level  : {s['alert_level']}
Power        : {s['power']} W
Voltage      : {s['voltage']} V
Current      : {s['current']} A
Energy Today : {s['energy_kwh']} kWh
Cost Today   : ₹{s['cost_today']}
Anomaly      : {'YES' if s['anomaly'] else 'NO'}

ACTION: Relay auto-switched OFF to prevent overload.

— AI Smart Energy Management System
  Karunya Institute of Technology and Sciences
"""

    def _email(self, subject, body):
        cfg = self.cfg.get('email', {})
        if not cfg.get('enabled'):
            print(f"[AlertSystem] Email disabled. Alert: {subject}")
            return
        try:
            msg            = MIMEMultipart()
            msg['From']    = cfg['sender']
            msg['To']      = cfg['recipient']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
                s.login(cfg['sender'], cfg['password'])
                s.send_message(msg)
            print("[AlertSystem] Email sent.")
        except Exception as e:
            print(f"[AlertSystem] Email error: {e}")

    def _sms(self, body):
        cfg = self.cfg.get('twilio', {})
        if not cfg.get('enabled'):
            return
        try:
            from twilio.rest import Client
            Client(cfg['account_sid'], cfg['auth_token']).messages.create(
                body=body, from_=cfg['from_number'], to=cfg['to_number'])
            print("[AlertSystem] SMS sent.")
        except Exception as e:
            print(f"[AlertSystem] SMS error: {e}")
