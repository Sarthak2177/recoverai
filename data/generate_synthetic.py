"""
RecoverAI — Synthetic Transaction Data Generator
"""
import json
import random
import string
import os
from datetime import datetime, timedelta

CUSTOMER_FIRST_NAMES = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan", "Ananya", "Diya", "Priya", "Meera", "Riya", "Kavya", "Neha", "Pooja", "Shreya", "Tanvi", "Rahul", "Amit", "Rohit", "Vikram", "Suresh", "Deepak", "Manish", "Rajesh", "Nikhil", "Akash", "Sneha", "Swati"]
CUSTOMER_LAST_NAMES = ["Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Shah", "Reddy", "Nair", "Iyer", "Joshi", "Mehta", "Chopra", "Malhotra", "Bhat", "Rao", "Das", "Mukherjee", "Banerjee", "Pillai", "Agarwal", "Saxena", "Kapoor", "Thakur", "Chauhan", "Dubey", "Tiwari", "Mishra", "Pandey", "Yadav"]
EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "rediffmail.com"]
CARD_BANKS = ["HDFC", "ICICI", "SBI", "Axis", "Kotak", "Yes Bank", "PNB", "BOB", "IndusInd", "RBL"]
UPI_APPS = ["gpay", "phonepe", "paytm", "bhim", "amazonpay", "cred"]
PRODUCT_NAMES = ["Premium Plan Subscription", "Annual Membership", "Course Bundle", "Enterprise License", "Pro Toolkit", "Cloud Storage 1TB", "VPN Annual", "Design Suite Pro", "Analytics Dashboard", "API Access Plan", "Wireless Earbuds", "Smart Watch Pro", "Laptop Stand", "Mechanical Keyboard", "USB-C Hub", "Portable SSD 500GB", "Webcam HD", "Noise Cancelling Headphones", "Fitness Tracker", "Smart Speaker", "Phone Case Premium", "Screen Protector Pack", "Bluetooth Mouse", "LED Desk Lamp", "Power Bank 20000mAh"]
BUSINESS_NAMES = ["TechFlow Solutions", "DigitalCraft India", "CloudNine Systems", "InnovateTech Labs", "PayScale Pro", "DataMind Analytics", "SwiftPay Commerce", "NexGen Software", "BrightPath Education", "HealthFirst Clinic", "GreenLeaf Organics", "UrbanStyle Fashion"]

PAYMENT_FAILURE_REASONS = [
    {"code": "CARD_DECLINED", "description": "Card declined by issuing bank", "recoverable": True},
    {"code": "INSUFFICIENT_FUNDS", "description": "Insufficient funds in account", "recoverable": True},
    {"code": "NETWORK_ERROR", "description": "Payment network timeout", "recoverable": True},
    {"code": "BANK_REFUSED", "description": "Transaction refused by bank", "recoverable": True},
    {"code": "EXPIRED_CARD", "description": "Card has expired", "recoverable": True},
    {"code": "INTERNATIONAL_BLOCKED", "description": "International transactions blocked on card", "recoverable": False},
    {"code": "INVALID_CVV", "description": "Incorrect CVV entered", "recoverable": True},
    {"code": "3DS_FAILED", "description": "3D Secure authentication failed", "recoverable": True},
    {"code": "RISK_CHECK_FAILED", "description": "Transaction flagged by risk engine", "recoverable": False},
    {"code": "BANK_DOWNTIME", "description": "Issuing bank systems unavailable", "recoverable": True},
]

CHECKOUT_ABANDON_STAGES = [
    {"stage": "CART_BUILT", "description": "Customer added items to cart but didn't proceed"},
    {"stage": "ADDRESS_ENTERED", "description": "Customer entered address but didn't continue to payment"},
    {"stage": "PAYMENT_PAGE", "description": "Customer reached payment page but didn't complete"},
    {"stage": "OTP_PENDING", "description": "Customer entered card details but abandoned at OTP"},
    {"stage": "UPI_PENDING", "description": "Customer selected UPI but didn't complete the mandate"},
]

SUBSCRIPTION_FAILURE_REASONS = [
    {"code": "RECURRING_DECLINED", "description": "Recurring charge declined by bank", "recoverable": True},
    {"code": "CARD_EXPIRED_SUB", "description": "Card on file has expired", "recoverable": True},
    {"code": "MANDATE_REVOKED", "description": "Customer revoked UPI autopay mandate", "recoverable": False},
    {"code": "INSUFFICIENT_FUNDS_SUB", "description": "Insufficient funds for subscription charge", "recoverable": True},
    {"code": "ACCOUNT_CLOSED", "description": "Bank account linked to subscription is closed", "recoverable": False},
    {"code": "PAYMENT_METHOD_REMOVED", "description": "Saved payment method no longer valid", "recoverable": True},
]

INVOICE_OVERDUE_REASONS = [
    {"code": "NOT_VIEWED", "description": "Invoice has not been opened by customer"},
    {"code": "DISPUTED", "description": "Customer disputes the invoice amount"},
    {"code": "PARTIAL_PAYMENT", "description": "Customer made partial payment only"},
    {"code": "PAYMENT_PENDING", "description": "Customer acknowledged but payment pending"},
    {"code": "CONTACT_UNREACHABLE", "description": "Unable to reach customer for follow-up"},
]

CUSTOMER_SEGMENTS = ["new", "returning", "premium", "enterprise", "at_risk"]
PAYMENT_METHODS = ["card", "upi", "netbanking", "wallet", "emi"]

def generate_id(prefix: str, length: int = 8) -> str:
    chars = string.ascii_lowercase + string.digits
    return f"{prefix}_{''.join(random.choices(chars, k=length))}"

def generate_razorpay_id(prefix: str = "pay") -> str:
    chars = string.ascii_uppercase + string.digits
    return f"{prefix}_{''.join(random.choices(chars, k=14))}"

def generate_customer() -> dict:
    first = random.choice(CUSTOMER_FIRST_NAMES)
    last = random.choice(CUSTOMER_LAST_NAMES)
    email = f"{first.lower()}.{last.lower()}{random.randint(1, 99)}@{random.choice(EMAIL_DOMAINS)}"
    phone = f"+91{random.randint(7000000000, 9999999999)}"
    return {
        "name": f"{first} {last}",
        "email": email,
        "phone": phone,
        "segment": random.choice(CUSTOMER_SEGMENTS),
        "lifetime_value": round(random.uniform(500, 150000), 2),
        "previous_purchases": random.randint(0, 50),
        "dnd_enabled": random.random() < 0.05,
        "preferred_contact": random.choice(["email", "sms", "whatsapp"]),
        "preferred_payment": random.choice(PAYMENT_METHODS),
        "city": random.choice(["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Jaipur", "Ahmedabad", "Lucknow"]),
    }

def generate_payment_failure(txn_id: int, base_time: datetime) -> dict:
    failure = random.choice(PAYMENT_FAILURE_REASONS)
    amount = random.choice([round(random.uniform(99, 999), 2), round(random.uniform(1000, 9999), 2), round(random.uniform(10000, 49999), 2), round(random.uniform(50000, 200000), 2)])
    payment_method = random.choice(PAYMENT_METHODS)
    customer = generate_customer()
    timestamp = base_time - timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))
    method_details = {}
    if payment_method == "card":
        bank = random.choice(CARD_BANKS)
        method_details = {"card_type": random.choice(["visa", "mastercard", "rupay"]), "card_last4": f"{random.randint(1000, 9999)}", "issuing_bank": bank, "card_category": random.choice(["debit", "credit"])}
    elif payment_method == "upi":
        method_details = {"vpa": f"{customer['name'].split()[0].lower()}@{random.choice(UPI_APPS)}"}
    elif payment_method == "netbanking":
        method_details = {"bank": random.choice(CARD_BANKS)}

    return {
        "id": f"TXN-{txn_id:04d}",
        "type": "payment_failure",
        "amount": amount,
        "currency": "INR",
        "status": "failed",
        "failure_reason": failure,
        "customer": customer,
        "payment_method": payment_method,
        "method_details": method_details,
        "product": random.choice(PRODUCT_NAMES),
        "razorpay_payment_id": generate_razorpay_id("pay"),
        "razorpay_order_id": generate_razorpay_id("order"),
        "timestamp": timestamp.isoformat(),
        "metadata": {"attempt_number": random.randint(1, 3), "session_duration_seconds": random.randint(30, 600), "device": random.choice(["mobile_android", "mobile_ios", "desktop_chrome", "desktop_firefox"]), "ip_country": "IN"}
    }

def generate_checkout_abandonment(txn_id: int, base_time: datetime) -> dict:
    stage = random.choice(CHECKOUT_ABANDON_STAGES)
    num_items = random.randint(1, 5)
    items = random.sample(PRODUCT_NAMES, min(num_items, len(PRODUCT_NAMES)))
    amount = round(sum(random.uniform(299, 9999) for _ in items), 2)
    customer = generate_customer()
    timestamp = base_time - timedelta(hours=random.randint(0, 48), minutes=random.randint(0, 59))

    return {
        "id": f"TXN-{txn_id:04d}",
        "type": "checkout_abandonment",
        "amount": amount,
        "currency": "INR",
        "status": "abandoned",
        "failure_reason": {"code": stage["stage"], "description": stage["description"], "recoverable": True},
        "customer": customer,
        "payment_method": None,
        "method_details": {},
        "product": ", ".join(items),
        "razorpay_payment_id": None,
        "razorpay_order_id": generate_razorpay_id("order"),
        "timestamp": timestamp.isoformat(),
        "metadata": {"cart_items": len(items), "cart_value": amount, "session_duration_seconds": random.randint(60, 1800), "pages_visited": random.randint(2, 12), "device": random.choice(["mobile_android", "mobile_ios", "desktop_chrome", "desktop_firefox"]), "referrer": random.choice(["google", "direct", "instagram", "facebook", "email_campaign"]), "coupon_applied": random.random() < 0.3, "abandon_stage": stage["stage"]}
    }

def generate_subscription_lapse(txn_id: int, base_time: datetime) -> dict:
    failure = random.choice(SUBSCRIPTION_FAILURE_REASONS)
    amount = random.choice([299, 499, 799, 999, 1499, 1999, 2999, 4999, 9999])
    customer = generate_customer()
    customer["segment"] = random.choice(["returning", "premium", "enterprise"])
    timestamp = base_time - timedelta(days=random.randint(0, 14), hours=random.randint(0, 23))
    months_active = random.randint(1, 36)

    return {
        "id": f"TXN-{txn_id:04d}",
        "type": "subscription_lapse",
        "amount": amount,
        "currency": "INR",
        "status": "lapsed",
        "failure_reason": failure,
        "customer": customer,
        "payment_method": random.choice(["card", "upi", "emandate"]),
        "method_details": {"subscription_id": generate_razorpay_id("sub"), "plan_name": random.choice(["Basic", "Pro", "Enterprise", "Premium", "Starter"]), "billing_cycle": random.choice(["monthly", "quarterly", "annual"]), "months_active": months_active, "total_paid": amount * months_active},
        "product": random.choice(PRODUCT_NAMES[:10]),
        "razorpay_payment_id": generate_razorpay_id("pay"),
        "razorpay_order_id": None,
        "timestamp": timestamp.isoformat(),
        "metadata": {"consecutive_failures": random.randint(1, 3), "last_successful_charge": (timestamp - timedelta(days=random.randint(30, 90))).isoformat(), "plan_mrr": amount, "churn_risk_score": round(random.uniform(0.3, 0.95), 2)}
    }

def generate_overdue_invoice(txn_id: int, base_time: datetime) -> dict:
    reason = random.choice(INVOICE_OVERDUE_REASONS)
    amount = random.choice([round(random.uniform(5000, 25000), 2), round(random.uniform(25000, 100000), 2), round(random.uniform(100000, 500000), 2)])
    days_overdue = random.choice([7, 14, 21, 30, 45, 60, 90])
    customer = generate_customer()
    customer["segment"] = random.choice(["enterprise", "premium"])
    due_date = base_time - timedelta(days=days_overdue)
    issued_date = due_date - timedelta(days=random.randint(15, 30))
    partial_paid = round(amount * random.uniform(0.1, 0.6), 2) if reason["code"] == "PARTIAL_PAYMENT" else 0

    return {
        "id": f"TXN-{txn_id:04d}",
        "type": "overdue_invoice",
        "amount": amount,
        "currency": "INR",
        "status": "overdue",
        "failure_reason": reason,
        "customer": customer,
        "payment_method": None,
        "method_details": {"invoice_id": generate_razorpay_id("inv"), "invoice_number": f"INV-{random.randint(2024, 2026)}-{random.randint(1000, 9999)}", "issued_date": issued_date.isoformat(), "due_date": due_date.isoformat(), "days_overdue": days_overdue, "partial_amount_paid": partial_paid, "outstanding_amount": round(amount - partial_paid, 2), "business_name": random.choice(BUSINESS_NAMES)},
        "product": f"Invoice for {random.choice(['consulting services', 'software license', 'API usage', 'support contract', 'implementation fee', 'maintenance agreement'])}",
        "razorpay_payment_id": None,
        "razorpay_order_id": None,
        "timestamp": base_time.isoformat(),
        "metadata": {"reminders_sent": random.randint(0, 3), "last_reminder_date": (base_time - timedelta(days=random.randint(1, 7))).isoformat() if random.random() > 0.3 else None, "customer_responded": random.random() < 0.4, "escalation_level": random.choice(["none", "manager", "finance_head"])}
    }

def generate_dataset(num_transactions: int = 200, seed: int = 42) -> list[dict]:
    random.seed(seed)
    base_time = datetime(2026, 8, 27, 12, 0, 0)
    transactions = []
    txn_id = 1
    n_payment = int(num_transactions * 0.40)
    n_checkout = int(num_transactions * 0.25)
    n_subscription = int(num_transactions * 0.20)
    n_invoice = num_transactions - n_payment - n_checkout - n_subscription

    for _ in range(n_payment):
        transactions.append(generate_payment_failure(txn_id, base_time))
        txn_id += 1
    for _ in range(n_checkout):
        transactions.append(generate_checkout_abandonment(txn_id, base_time))
        txn_id += 1
    for _ in range(n_subscription):
        transactions.append(generate_subscription_lapse(txn_id, base_time))
        txn_id += 1
    for _ in range(n_invoice):
        transactions.append(generate_overdue_invoice(txn_id, base_time))
        txn_id += 1

    random.shuffle(transactions)
    return transactions

def main():
    transactions = generate_dataset(num_transactions=200)
    output_path = os.path.join(os.path.dirname(__file__), "transactions.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)

    type_counts = {}
    total_amount = 0
    for txn in transactions:
        t = txn["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
        total_amount += txn["amount"]

    print(f"Success: Generated {len(transactions)} transactions")
    print(f"Total revenue at risk: INR {total_amount:,.2f}")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
