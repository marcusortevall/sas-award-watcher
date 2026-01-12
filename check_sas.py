import requests, os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def notify(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT, "text": msg})

def check(date):
    for cabin in ["ECONOMY", "PREMIUM"]:
        payload = {
            "origin": "ARN",
            "destination": "ICN",
            "date": date,
            "cabin": cabin,
            "adults": 2
        }

        r = requests.post(
            "https://api.flysas.com/booking/award/search",
            json=payload,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        data = r.json()

        for f in data.get("flights", []):
            if f.get("awardSeats", 0) >= 2:
                notify(
                    f"🎉 SAS AWARD FOUND\n"
                    f"{date}\n"
                    f"{cabin}\n"
                    f"{f['flightNumber']}\n"
                    f"2 seats available"
                )
                return True
    return False

for day in range(1, 31):
    date = f"2026-09-{day:02d}"
    check(date)
