import time
import requests
import logging
import json
import os
import re
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TimedOut
import asyncio
import random
from datetime import datetime, timedelta

# ========= CONFIG =========
BOT_TOKEN = '7354539559:AAGGAgOmdZx-a_TC75nh_uF_ngVN5n-yQEs'
CHAT_ID = '-1003712306038'
USERNAME = 'abcd1234'
PASSWORD = 'abcd1234'
BASE_URL = "http://139.99.208.63"
LOGIN_PAGE_URL = BASE_URL + "/ints/login"
LOGIN_POST_URL = BASE_URL + "/ints/signin"
DATA_URL = BASE_URL + "/ints/client/res/data_smscdr.php"

bot = Bot(token=BOT_TOKEN)
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})
logging.basicConfig(level=logging.INFO, format='%(message)s')

os.system('cls' if os.name == 'nt' else 'clear')

# ========= COUNTRY MAP =========
COUNTRY_MAP = {  # একইটা রাখলাম, সংক্ষেপের জন্য এখানে দিচ্ছি না
    '1': '🇺🇸 USA / Canada',
    '880': '🇧🇩 Bangladesh',
    '91': '🇮🇳 India',
    "1": ("🇺🇸", "USA / Canada"),
    "7": ("🇷🇺", "Russia / Kazakhstan"),
    "20": ("🇪🇬", "Egypt"),
    "27": ("🇿🇦", "South Africa"),
    "30": ("🇬🇷", "Greece"),
    "31": ("🇳🇱", "Netherlands"),
    "32": ("🇧🇪", "Belgium"),
    "33": ("🇫🇷", "France"),
    "34": ("🇪🇸", "Spain"),
    "36": ("🇭🇺", "Hungary"),
    "39": ("🇮🇹", "Italy"),
    "40": ("🇷🇴", "Romania"),
    "41": ("🇨🇭", "Switzerland"),
    "43": ("🇦🇹", "Austria"),
    "44": ("🇬🇧", "United Kingdom"),
    "45": ("🇩🇰", "Denmark"),
    "46": ("🇸🇪", "Sweden"),
    "47": ("🇳🇴", "Norway"),
    "48": ("🇵🇱", "Poland"),
    "49": ("🇩🇪", "Germany"),
    "51": ("🇵🇪", "Peru"),
    "52": ("🇲🇽", "Mexico"),
    "53": ("🇨🇺", "Cuba"),
    "54": ("🇦🇷", "Argentina"),
    "55": ("🇧🇷", "Brazil"),
    "56": ("🇨🇱", "Chile"),
    "57": ("🇨🇴", "Colombia"),
    "58": ("🇻🇪", "Venezuela"),
    "60": ("🇲🇾", "Malaysia"),
    "61": ("🇦🇺", "Australia"),
    "62": ("🇮🇩", "Indonesia"),
    "63": ("🇵🇭", "Philippines"),
    "64": ("🇳🇿", "New Zealand"),
    "65": ("🇸🇬", "Singapore"),
    "66": ("🇹🇭", "Thailand"),
    "81": ("🇯🇵", "Japan"),
    "82": ("🇰🇷", "South Korea"),
    "84": ("🇻🇳", "Vietnam"),
    "86": ("🇨🇳", "China"),
    "90": ("🇹🇷", "Turkey"),
    "91": ("🇮🇳", "India"),
    "92": ("🇵🇰", "Pakistan"),
    "93": ("🇦🇫", "Afghanistan"),
    "94": ("🇱🇰", "Sri Lanka"),
    "95": ("🇲🇲", "Myanmar"),
    "98": ("🇮🇷", "Iran"),
    "211": ("🇸🇸", "South Sudan"),
    "212": ("🇲🇦", "Morocco"),
    "213": ("🇩🇿", "Algeria"),
    "216": ("🇹🇳", "Tunisia"),
    "218": ("🇱🇾", "Libya"),
    "220": ("🇬🇲", "Gambia"),
    "221": ("🇸🇳", "Senegal"),
    "222": ("🇲🇷", "Mauritania"),
    "223": ("🇲🇱", "Mali"),
    "224": ("🇬🇳", "Guinea"),
    "225": ("🇨🇮", "Côte d'Ivoire"),
    "226": ("🇧🇫", "Burkina Faso"),
    "227": ("🇳🇪", "Niger"),
    "228": ("🇹🇬", "Togo"),
    "229": ("🇧🇯", "Benin"),
    "230": ("🇲🇺", "Mauritius"),
    "231": ("🇱🇷", "Liberia"),
    "232": ("🇸🇱", "Sierra Leone"),
    "233": ("🇬🇭", "Ghana"),
    "234": ("🇳🇬", "Nigeria"),
    "235": ("🇹🇩", "Chad"),
    "236": ("🇨🇫", "Central African Republic"),
    "237": ("🇨🇲", "Cameroon"),
    "238": ("🇨🇻", "Cape Verde"),
    "239": ("🇸🇹", "Sao Tome & Principe"),
    "240": ("🇬🇶", "Equatorial Guinea"),
    "241": ("🇬🇦", "Gabon"),
    "242": ("🇨🇬", "Congo"),
    "243": ("🇨🇩", "DR Congo"),
    "244": ("🇦🇴", "Angola"),
    "249": ("🇸🇩", "Sudan"),
    "250": ("🇷🇼", "Rwanda"),
    "251": ("🇪🇹", "Ethiopia"),
    "252": ("🇸🇴", "Somalia"),
    "253": ("🇩🇯", "Djibouti"),
    "254": ("🇰🇪", "Kenya"),
    "255": ("🇹🇿", "Tanzania"),
    "256": ("🇺🇬", "Uganda"),
    "257": ("🇧🇮", "Burundi"),
    "258": ("🇲🇿", "Mozambique"),
    "260": ("🇿🇲", "Zambia"),
    "261": ("🇲🇬", "Madagascar"),
    "263": ("🇿🇼", "Zimbabwe"),
    "264": ("🇳🇦", "Namibia"),
    "265": ("🇲🇼", "Malawi"),
    "266": ("🇱🇸", "Lesotho"),
    "267": ("🇧🇼", "Botswana"),
    "268": ("🇸🇿", "Eswatini"),
    "269": ("🇰🇲", "Comoros"),
    "290": ("🇸🇭", "Saint Helena"),
    "291": ("🇪🇷", "Eritrea"),
    "297": ("🇦🇼", "Aruba"),
    "298": ("🇫🇴", "Faroe Islands"),
    "299": ("🇬🇱", "Greenland"),
    "350": ("🇬🇮", "Gibraltar"),
    "351": ("🇵🇹", "Portugal"),
    "352": ("🇱🇺", "Luxembourg"),
    "353": ("🇮🇪", "Ireland"),
    "354": ("🇮🇸", "Iceland"),
    "355": ("🇦🇱", "Albania"),
    "356": ("🇲🇹", "Malta"),
    "357": ("🇨🇾", "Cyprus"),
    "358": ("🇫🇮", "Finland"),
    "359": ("🇧🇬", "Bulgaria"),
    "370": ("🇱🇹", "Lithuania"),
    "371": ("🇱🇻", "Latvia"),
    "372": ("🇪🇪", "Estonia"),
    "373": ("🇲🇩", "Moldova"),
    "374": ("🇦🇲", "Armenia"),
    "375": ("🇧🇾", "Belarus"),
    "376": ("🇦🇩", "Andorra"),
    "377": ("🇲🇨", "Monaco"),
    "378": ("🇸🇲", "San Marino"),
    "380": ("🇺🇦", "Ukraine"),
    "381": ("🇷🇸", "Serbia"),
    "382": ("🇲🇪", "Montenegro"),
    "383": ("🇽🇰", "Kosovo"),
    "385": ("🇭🇷", "Croatia"),
    "386": ("🇸🇮", "Slovenia"),
    "387": ("🇧🇦", "Bosnia & Herzegovina"),
    "389": ("🇲🇰", "North Macedonia"),
    "420": ("🇨🇿", "Czech Republic"),
    "421": ("🇸🇰", "Slovakia"),
    "423": ("🇱🇮", "Liechtenstein"),
    "852": ("🇭🇰", "Hong Kong"),
    "853": ("🇲🇴", "Macau"),
    "855": ("🇰🇭", "Cambodia"),
    "856": ("🇱🇦", "Laos"),
    "880": ("🇧🇩", "Bangladesh"),
    "886": ("🇹🇼", "Taiwan"),
    "960": ("🇲🇻", "Maldives"),
    "961": ("🇱🇧", "Lebanon"),
    "962": ("🇯🇴", "Jordan"),
    "963": ("🇸🇾", "Syria"),
    "964": ("🇮🇶", "Iraq"),
    "965": ("🇰🇼", "Kuwait"),
    "966": ("🇸🇦", "Saudi Arabia"),
    "967": ("🇾🇪", "Yemen"),
    "968": ("🇴🇲", "Oman"),
    "970": ("🇵🇸", "Palestine"),
    "971": ("🇦🇪", "UAE"),
    "972": ("🇮🇱", "Israel"),
    "973": ("🇧🇭", "Bahrain"),
    "974": ("🇶🇦", "Qatar"),
    "975": ("🇧🇹", "Bhutan"),
    "976": ("🇲🇳", "Mongolia"),
    "977": ("🇳🇵", "Nepal"),
    "992": ("🇹🇯", "Tajikistan"),
    "993": ("🇹🇲", "Turkmenistan"),
    "994": ("🇦🇿", "Azerbaijan"),
    "995": ("🇬🇪", "Georgia"),
    "996": ("🇰🇬", "Kyrgyzstan"),
    "998": ("🇺🇿", "Uzbekistan"),
    # ... অন্যান্য কোডগুলো আগের মতো থাকবে
}

# ========= FUNNY STATUS =========
FUNNY_STATUS_DICT = {
    "default": [
        "OTP আসছে মানে আজ ভাগ্য জেগে উঠছে 😎",
        "OTP দেখেই বুঝি—সিস্টেম জীবিত 🔥",
        "OTP পাইছি, টেনশন নাই 😁",
        "OTP মানেই বিজয়ের শুরু 🏆"
        "OTP আসছে মানে আজ ভাগ্য জেগে উঠছে 😎",
    "OTP দেখেই বুঝি—সিস্টেম জীবিত 🔥",
    "OTP পাইছি, টেনশন নাই 😁",
    "OTP মানেই বিজয়ের শুরু 🏆",
    "OTP আসছে, বস এখন খুশি 😌",
    "OTP ডেলিভারি সফল 📩",
    "OTP এলো মানে সিস্টেম অন 😜",
    "OTP এলেই উৎসব 🎉",
    "OTP পাইছি, আর কি চাই 😎",
    "OTP না এলে ঘুম নাই 😴",
    "OTP এলেই মন ফ্রেশ 😄",
    "আরেকটা OTP, আরেক ধাপ এগিয়ে 💪",
    "OTP দেখেই কাজ শুরু 🚀",
    "কোড এসেছে, এখন action 😎",
    "OTP পাইছি, বস খুশি 😁",
    "OTP আসছে মানে আজ ভাগ্য জেগে উঠছে 😎",
    "OTP দেখেই বুঝি—সিস্টেম জীবিত 🔥",
    "OTP এলো, কাজ চললো 💪",
    "OTP পাইছি, টেনশন নাই 😁",
    "OTP মানেই বিজয়ের শুরু 🏆",
    "OTP আসছে, বস এখন খুশি 😌",
    "OTP ডেলিভারি সফল 📩",
    "OTP এলো মানে সার্ভার ঠিক আছে 😜",
    "OTP পাইছি ভাই, আর কি চাই 😎",
    "OTP না এলে ঘুম নাই 😴",
    "OTP এলেই মন ভালো 😄",
    "OTP = Happiness 😆",
    "OTP দেখেই হাসি চলে আসে 😁",
    "OTP মানে আজ লাকি ডে 🍀",
    "OTP আসছে, কাজ চলছে 🔄",
    "OTP পেলেই চাপ শেষ 😌",
    "OTP এলো মানে সিস্টেম অন 🔥",
    "OTP পাইছি, বস খুশি 😎",
    "OTP এলেই উৎসব 🎉",
    "OTP মানে সব ঠিকঠাক 👍",
    "OTP দেখেই বোঝা যায় বট কাজ করছে 🤖",
    "OTP এলেই দিন সফল ☀️",
    "OTP মানে আজ আর ঘুম নাই 😜",
    "OTP এলো—মুড অন 😁",
    "OTP পাইছি, ব্যাস 😎",
    "OTP এলো মানে প্রগ্রেস 📈",
    "OTP না এলে মন খারাপ 😢",
    "OTP দেখেই হালকা হাসি 😄",
    "OTP আসছে—সিগন্যাল ক্লিয়ার 📶",
    "OTP মানে সাফল্যের গন্ধ 😆",
    "OTP পাইছি ভাই, চা দাও ☕",
    "OTP আসছে মানে খেল খতম 🔥",
    "OTP এলো, কাজ জমে উঠছে 💪",
    "OTP দেখেই আত্মবিশ্বাস 😎",
    "OTP এলো—সব ঠিক 👍",
    "OTP পাইছি, বস approve 😁",
    "OTP মানে মিশন অন 🎯",
    "OTP এলো, আজ কাজের দিন 😄",
    "OTP না এলে মন বসে না 😜",
    "OTP এলো—সিস্টেম হাসছে 🤖",
    "OTP পাইছি, আলহামদুলিল্লাহ 🙏",
    "OTP আসছে, গেম অন 🔥",
    "OTP দেখেই বুঝি সব লাইভ 🟢",
    "OTP মানেই আজ কাজ চলছে 😎",
    "OTP এলো—টেনশন অফ ❌",
    "OTP পাইছি, ব্যাস শান্তি 😌",
    "OTP মানে সব ঠিকঠাক 🧠",
    "OTP এলো—মুড ভালো 😁",
    "OTP দেখেই মন ফুরফুরে 😆",
    "OTP মানে সার্ভার বেঁচে আছে 💻",
    "OTP আসছে—চাপ নাই 😄",
    "OTP পাইছি, আর কি লাগে 😎",
    "OTP এলো—হাসি অন 😁",
    "OTP মানে সিস্টেম রাজা 👑",
    "OTP এলো—সবুজ সংকেত 🟢",
    "OTP দেখেই দিন সুন্দর ☀️",
    "OTP পাইছি, বস সন্তুষ্ট 😌",
    "OTP মানে কাজের প্রমাণ 📌",
    "OTP এলো—মন ভালো 😄",
    "OTP না এলে চা খেতে মন চায় না ☕",
    "OTP আসছে—মিশন চলছে 🎯",
    "OTP দেখেই বুঝি স্ক্রিপ্ট ঠিক 😎",
    "OTP মানে আজ আর চিন্তা নাই 😁",
    "OTP এলো—ডিউটি ফুল অন 🔥",
    "OTP পাইছি, হাসি থামছে না 😄",
    "OTP মানে কাজের ফল 🍎",
    "OTP এলো—সিস্টেম হ্যাপি 🤖",
    "OTP দেখেই বোঝা যায় সব অন 🟢",
    "OTP মানে আজ ভালো দিন 😆",
    "OTP এলো—মন শান্ত 😌",
    "OTP আসছে—খেলা জমে উঠছে 🔥",
    "OTP পাইছি, বস খুশি 😎",
    "OTP মানে কাজ চলছে 💪",
    "OTP এলো—সব ঠিকঠাক 👍",
    "OTP দেখেই মনে শান্তি 😄",
    "OTP মানে স্ক্রিপ্ট জীবিত 🤖",
    "OTP এলো—টেনশন শেষ ❌",
    "OTP পাইছি, আলাদা সুখ 😁",
    "OTP মানে আজ লাকি 🍀",
    "OTP এলো—সবুজ বাতি 🟢",
    "OTP আসছে—সিস্টেম হাসছে 😆",
    "OTP দেখেই মন ভালো 😄",
    "OTP মানে কাজ ঠিক পথে 🎯",
    "OTP এলো—চাপ কম 😌",
    "OTP পাইছি, বস approve 😎",
    "OTP মানে আজ কাজের দিন 💪",
    "OTP এলো—হালকা খুশি 😁",
    "OTP দেখেই বোঝা যায় লাইভ 🟢",
    "OTP মানে স্ক্রিপ্ট সফল 🔥",
    "OTP এলো—মন চাঙ্গা 😄",
    "OTP আসছে—সব অন ট্র্যাক 🎯",
    "OTP পাইছি, আরাম 😌",
    "OTP মানে কাজ চলছে 😎",
    "OTP এলো—হাসি চলে আসে 😁",
    "OTP দেখেই আত্মবিশ্বাস 💪",
    "OTP মানে সিস্টেম ঠিক 👍",
    "OTP এলো—মুড অন 😆",
    "OTP পাইছি, দিন ভালো ☀️",
    "OTP মানে কাজের সুখ 😄",
    "OTP এলো—সব ঠিক আছে 🔥",
    "আরেকটা OTP, আরেক ধাপ এগিয়ে 💪"
        # ... আগের মতো অন্যান্য status
    ]
}

# ========= UTILITIES =========
def get_country_from_number(number:str)->str:
    for code in sorted(COUNTRY_MAP.keys(), key=lambda x: -len(x)):
        if number.startswith(code):
            return COUNTRY_MAP[code]
    return '🌍 Unknown'

def escape_html(text:str)->str:
    return text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def save_already_sent(already_sent):
    with open("already_sent.json","w") as f:
        json.dump(list(already_sent),f)

def load_already_sent():
    if os.path.exists("already_sent.json"):
        with open("already_sent.json","r") as f:
            return set(json.load(f))
    return set()

already_sent = load_already_sent()
otp_funny_map = {}

def get_funny_status(otp, service):
    status_list = FUNNY_STATUS_DICT.get(service, FUNNY_STATUS_DICT["default"])
    used_status = otp_funny_map.get(otp,set())
    available_status = [s for s in status_list if s not in used_status]
    if not available_status:
        used_status = set()
        available_status = status_list.copy()
    funny_status = random.choice(available_status)
    used_status.add(funny_status)
    otp_funny_map[otp] = used_status
    return funny_status

# ========= LOGIN (CMD & IDE friendly) =========
def login():
    try:
        resp = session.get(LOGIN_PAGE_URL)
        resp.encoding = 'utf-8'  # CMD তেও ঠিকভাবে decode হবে
        
        # Debug: CMD তে login page preview
        print("=== LOGIN PAGE PREVIEW ===")
        print(resp.text[:500])
        print("==========================")
        
        match = re.search(r'What is (\d+) \+ (\d+)', resp.text)
        if not match:
            logging.error("Captcha not found. Login failed ❌")
            return False
        captcha_answer = int(match.group(1)) + int(match.group(2))
        
        payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "capt": captcha_answer
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": LOGIN_PAGE_URL,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36"
        }
        
        resp = session.post(LOGIN_POST_URL, data=payload, headers=headers)
        
        # Debug: POST response preview
        print("=== LOGIN POST RESPONSE PREVIEW ===")
        print(resp.status_code)
        print(resp.text[:500])
        print("==========================")
        
        if "dashboard" in resp.text.lower() or "logout" in resp.text.lower():
            logging.info("Login successful ✅")
            return True
        else:
            logging.error("Login failed ❌")
            return False

    except Exception as e:
        logging.error(f"Login error: {e}")
        return False

# ========= FETCH DATA =========
def build_api_url():
    start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    return (f"{DATA_URL}?fdate1={start_date}%2000:00:00&fdate2={end_date}%2023:59:59&"
            "frange=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgnumber=&fgcli=&fg=0&"
            "sEcho=1&iColumns=7&sColumns=%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&"
            "mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&"
            "mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&"
            "mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&"
            "mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&"
            "mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&"
            "mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&"
            "mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&"
            "sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1")

def fetch_data():
    url = build_api_url()
    headers = {"X-Requested-With":"XMLHttpRequest"}
    try:
        response = session.get(url, headers=headers, timeout=200)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 or "login" in response.text.lower():
            logging.warning("Session expired. Re-logging...")
            if login(): return fetch_data()
            return None
        else:
            logging.error(f"Unexpected error: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Fetch error: {e}")
        return None

# ========= SEND MESSAGES =========
async def sent_messages():
    logging.info("🔍 Checking for messages...\n")
    data = fetch_data()
    if data and 'aaData' in data:
        for row in data['aaData']:
            date = str(row[0]).strip()
            number = str(row[2]).strip()
            service = str(row[3]).strip()
            message = str(row[4]).strip()
            match = re.search(r'\d{3}-\d{3}|\d{4,6}', message)
            otp = match.group() if match else None
            if otp:
                unique_key = f"{number}|{otp}"
                if unique_key not in already_sent:
                    already_sent.add(unique_key)
                    country = get_country_from_number(number)
                    masked_number = number[:4] + "*"*(len(number)-10) + number[-4:]
                    funny_status = get_funny_status(otp, service)
                    text = (f"✨ <b>নতুন OTP পাওয়া গেছে!</b> ✨\n\n"
                            f"🌐 <b>Country:</b> {country}\n"
                            f"📞 <b>Number:</b> {masked_number}\n"
                            f"🔧 <b>Service:</b> {escape_html(service)}\n"
                            f"🔐 <b>OTP:</b> <code>{escape_html(otp)}</code>\n"
                            f"📝 <b>Message:</b> <i>{escape_html(message)}</i>\n\n"
                            f"💬 <i>{escape_html(funny_status)}</i>")
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("👨‍💻 Bot Owner", url="https://t.me/Ayanmalik00007")],
                        [InlineKeyboardButton("🔁 NUMBERS Channel", url="https://t.me/sharpzone0007")]
                    ])
                    try:
                        await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML",
                                               disable_web_page_preview=True, reply_markup=keyboard)
                        save_already_sent(already_sent)
                        logging.info(f"[+] Sent OTP: {otp}")
                    except TimedOut: logging.error("Telegram TimedOut")
                    except Exception as e: logging.error(f"Telegram error: {e}")
            else:
                logging.info(f"No OTP found in: {message}")
    else:
        logging.info("No data or invalid response.")

# ========= MAIN LOOP =========
async def main():
    if login():
        while True:
            await sent_messages()
            await asyncio.sleep(7)  # 20 sec delay CMD-safe
    else:
        logging.error("Initial login failed. Exiting...")

# ========= RUN =========
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user ✋")
