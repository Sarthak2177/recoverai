"""
RecoverAI — Razorpay API Client Wrapper
"""
import os
from dotenv import load_dotenv

load_dotenv()

class RazorpayClientWrapper:
    def __init__(self):
        self.key_id = os.getenv("RAZORPAY_KEY_ID")
        self.key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        self.is_configured = bool(self.key_id and self.key_secret)
        self.client = None
        
        if self.is_configured:
            try:
                import razorpay
                self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
                print("💳 Razorpay API Client initialized.")
            except Exception as e:
                print(f"❌ Error initializing Razorpay Client: {e}")
                self.is_configured = False
        else:
             print("⚠️ Razorpay keys not found. Client running in SIMULATION mode.")

    def create_payment_link(self, amount: int, currency: str, description: str, customer: dict):
        if not self.is_configured:
            return {"id": "plink_sim_12345", "short_url": "https://rzp.io/i/simulated"}
            
        try:
            return self.client.payment_link.create({
                "amount": amount * 100, # paise
                "currency": currency,
                "description": description,
                "customer": {
                    "name": customer.get("name", ""),
                    "email": customer.get("email", ""),
                    "contact": customer.get("phone", "")
                },
                "notify": {"sms": True, "email": True}
            })
        except Exception as e:
             return {"error": str(e)}

_instance = None

def get_rzp_client():
    global _instance
    if _instance is None:
        _instance = RazorpayClientWrapper()
    return _instance
