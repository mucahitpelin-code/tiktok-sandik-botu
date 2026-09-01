import asyncio
import aiohttp
import json
import requests

TELEGRAM_TOKEN = "8818251028:AAF71s67HYEej39MMvSNFEBSc0knnD8z5zA"
CHAT_ID = "-1003939640315"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Referer": "https://www.tiktok.com/live"
}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

def fetch_live_users():
    url = "https://www.tiktok.com/api/live/recommend/item_list/?aid=1988&count=50"
    users = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            items = data.get("data", []) or data.get("itemList", []) or []
            for item in items:
                author = item.get("author", {}) or item.get("owner", {})
                u_id = author.get("uniqueId") or author.get("unique_id")
                r_id = item.get("roomId") or item.get("room_id")
                if u_id and r_id:
                    users.append((u_id, str(r_id)))
    except Exception as e:
        print(f"Hata: {e}")
    return users

def check_chests():
    users = fetch_live_users()
    print(f"🌐 Bulutta {len(users)} Adet Canlı Yayın Yakalandı, Sandıklar Taranıyor...")
    
    for username, room_id in users:
        chest_url = f"https://webcast.tiktok.com/webcast/wallet_api/treasure_bag/list/?room_id={room_id}&aid=1988"
        try:
            res = requests.get(chest_url, headers=HEADERS, timeout=5)
            if res.status_code == 200:
                c_data = res.json()
                chests = c_data.get("data", {}).get("treasure_bag_list", []) or []
                for chest in chests:
                    time_left = chest.get("time_diff", 999)
                    if time_left < 72:
                        msg = (
                            f"🎁 **Sandık Bulundu!**\n\n"
                            f"👤 **Yayıncı:** @{username}\n"
                            f"⏳ **Kalan Süre:** {time_left} saniye\n\n"
                            f"🔗 https://www.tiktok.com/@{username}/live"
                        )
                        send_telegram(msg)
                        print(f"🔥 SANDIK DÜŞTÜ: @{username}")
        except Exception:
            pass

if __name__ == "__main__":
    check_chests()
      
