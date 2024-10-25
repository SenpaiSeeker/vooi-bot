import json
import time
import os
import random
from datetime import datetime
import urllib.parse
import cloudscraper
from colorama import Fore, Style, init
from dateutil import parser
from dateutil.tz import tzutc
from pyfiglet import Figlet

init(autoreset=True)

def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def interpolate_color(start_color, end_color, factor: float):
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * factor),
        int(start_color[1] + (end_color[1] - start_color[1]) * factor),
        int(start_color[2] + (end_color[2] - start_color[2]) * factor),
    )

def print_gradient_text(text, start_color, end_color):
    for i, char in enumerate(text):
        factor = i / len(text)
        r, g, b = interpolate_color(start_color, end_color, factor)
        print(rgb_to_ansi(r, g, b) + char, end="")
    print(Style.RESET_ALL)  # Reset colors after the text

class VooiDC:
    def __init__(self):
        self.base_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/json",
            "Origin": "https://app.tg.vooi.io",
            "Referer": "https://app.tg.vooi.io/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        self.scraper = cloudscraper.create_scraper()
        self.access_token = None
    start_color = (230, 230, 250)  # Lavender color for lighter purple
    end_color = (128, 0, 128)      # Purple
    def display_banner():
        custom_fig = Figlet(font='slant')
        if os.name == "nt":
            custom_fig = Figlet(font='Stforek')
        os.system("title ASC AIRDROP " if os.name == "nt" else "clear")
        os.system("cls" if os.name == "nt" else "clear")
    
        print('')
        print_gradient_text(custom_fig.renderText('ASC AIRDROP'), VooiDC.start_color, VooiDC.end_color)
        print(f"{Fore.GREEN + Style.BRIGHT}!!! VOOI Mini Apps BOT !!!{Fore.RESET}")
        print(f"{Fore.GREEN + Style.BRIGHT}[+] Jika Mengalami Error!{Fore.RESET}")
        print(f"{Fore.YELLOW + Style.BRIGHT}[+] Silahkan Join Telegram : @airdropasc{Fore.RESET}")
        print('')
    def get_headers(self):
        headers = self.base_headers.copy()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def log(self, msg, type='info'):
        timestamp = datetime.now().strftime("%x %X %Z")
        if type == 'success':
            print(f"[{timestamp}] [*] {Fore.GREEN + Style.BRIGHT}{msg}")
        elif type == 'custom':
            print(f"[{timestamp}] [*] {Fore.MAGENTA + Style.BRIGHT}{msg}")
        elif type == 'error':
            print(f"[{timestamp}] [!] {Fore.RED + Style.BRIGHT}{msg}")
        elif type == 'warning':
            print(f"[{timestamp}] [*] {Fore.YELLOW + Style.BRIGHT}{msg}")
        else:
            print(f"[{timestamp}] [*] {Fore.BLUE + Style.BRIGHT}{msg}")

    def countdown(self, seconds):
        for i in range(seconds, -1, -1):
            print(f"\r===== Tunggu sebentar {i} detik untuk melanjutkan =====", end="", flush=True)
            time.sleep(1)
        print()

    def login_new_api(self, init_data):
        url = "https://api-tg.vooi.io/api/v2/auth/login"
        payload = {
            "initData": init_data,
            "inviterTelegramId": ""
        }

        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code == 201:
                self.access_token = response.json()['tokens']['access_token']
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": 'Unexpected response status'}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_autotrade(self):
        url = "https://api-tg.vooi.io/api/autotrade"
        try:
            response = self.scraper.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            return None

    def start_autotrade(self):
        url = "https://api-tg.vooi.io/api/autotrade/start"
        payload = {}
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
        except Exception as e:
            self.log(f"Error starting autotrade: {str(e)}", 'error')
            return None

    def claim_autotrade(self, auto_trade_id):
        url = "https://api-tg.vooi.io/api/autotrade/claim"
        payload = {"autoTradeId": auto_trade_id}
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
        except Exception as e:
            self.log(f"Error klaim autotrade: {str(e)}", 'error')
            return None

    def print_autotrade_info(self, data):
        end_time = parser.parse(data['endTime'])
        current_time = datetime.now(tzutc())
        time_left = end_time - current_time
        
        # Rounding the remaining time
        hours, remainder = divmod(time_left.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        rounded_time_left = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        self.log(f"Autotrade still running: {end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC", 'custom')
        self.log(f"Waktu tersisa: {rounded_time_left}", 'custom')

    def handle_autotrade(self):
        autotrade_data = self.check_autotrade()
        if not autotrade_data:
            self.log("Autotrade tidak berjalan. Memulai autotrade...", 'warning')
            autotrade_data = self.start_autotrade()
            if autotrade_data:
                self.print_autotrade_info(autotrade_data)
            else:
                self.log("Tidak dapat memulai Autotrade", 'error')
                return

        if autotrade_data['status'] == 'finished':
            self.log("Autotrade Selesai. Sedang klaim hadiah...", 'success')
            claim_result = self.claim_autotrade(autotrade_data['autoTradeId'])
            if claim_result:
                self.log(f"Sukses klaim autotrade. Mendapatkan {claim_result['reward']['virtMoney']} USD {claim_result['reward']['virtPoints']} VT", 'success')
                self.log(f"Total Saldo {claim_result['balance']['virt_money']} USDT | {claim_result['balance']['virt_points']} VT", 'success')
            else:
                self.log("Gagal klaim hadiah autotrade.", 'error')

            self.log("Memulai autotrade...", 'warning')
            new_autotrade_data = self.start_autotrade()
            if new_autotrade_data:
                self.print_autotrade_info(new_autotrade_data)
            else:
                self.log("Tidak dapat memulai Autotrade.", 'error')
        else:
            self.print_autotrade_info(autotrade_data)

    def start_tapping_session(self):
        url = "https://api-tg.vooi.io/api/tapping/start_session"
        payload = {}
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                return None
        except Exception as e:
            self.log(f"Gagal memulai sesi tap-tap: {str(e)}", 'error')
            return None

    def finish_tapping_session(self, session_id, virt_money, virt_points):
        url = "https://api-tg.vooi.io/api/tapping/finish"
        payload = {
            "sessionId": session_id,
            "tapped": {
                "virtMoney": virt_money,
                "virtPoints": virt_points
            }
        }
        try:
            response = self.scraper.post(url, json=payload, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.log(f"Status error saat memulai sesi tap-tap: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Error menyelesaikan sesi tap !: {str(e)}", 'error')
            return None

    def play_tapping_game(self):
        for game_number in range(1, 6):
            self.log(f"Memulai tap coin {game_number}/5", 'custom')
            session_data = self.start_tapping_session()
            if not session_data:
                self.log(f"Gagal memulai game {game_number}. Skipping game.", 'warning')
                continue

            virt_money_limit = int(session_data['config']['virtMoneyLimit'])
            virt_points_limit = int(session_data['config']['virtPointsLimit'])

            self.log(f"Tunggu beberapa detik untuk menyelesaikan tap-tap", 'custom')
            time.sleep(30)

            virt_money = random.randint(max(1, int(virt_money_limit * 0.5)), int(virt_money_limit * 0.8))
            virt_money = virt_money - (virt_money % 1)

            virt_points = 0
            if virt_points_limit > 0:
                virt_points = virt_points_limit

            result = self.finish_tapping_session(session_data['sessionId'], virt_money, virt_points)
            if result:
                self.log(f"Tap sukses, mendapatkan {result['tapped']['virtMoney']} USD | {result['tapped']['virtPoints']} VT", 'success')
            else:
                self.log(f"Tidak dapat menyelesaikan game {game_number}", 'error')

            if game_number < 5:
                self.log("Tunggu sebentar", 'custom')
                time.sleep(3)

    def get_tasks(self):
        url = "https://api-tg.vooi.io/api/tasks?limit=200&skip=0"
        try:
            response = self.scraper.get(url, headers=self.get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                self.log(f"Status error saat mengklaim tugas: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Error getting tasks: {str(e)}", 'error')
            return None

    def start_task(self, task_id):
        url = f"https://api-tg.vooi.io/api/tasks/start/{task_id}"
        try:
            response = self.scraper.post(url, json={}, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.log(f"Status error saat mengklaim tugas: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Gagal memulai tasks: {str(e)}", 'error')
            return None

    def claim_task(self, task_id):
        url = f"https://api-tg.vooi.io/api/tasks/claim/{task_id}"
        try:
            response = self.scraper.post(url, json={}, headers=self.get_headers())
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self.log(f"Status error saat mengklaim tugas: {response.status_code}", 'warning')
                return None
        except Exception as e:
            self.log(f"Gagal Klaim Task: {str(e)}", 'error')
            return None

    def manage_tasks(self):
        tasks_data = self.get_tasks()
        if not tasks_data:
            self.log("Gagal memulai tasks", 'error')
            return

        new_tasks = [task for task in tasks_data['nodes'] if task['status'] == 'new']
        for task in new_tasks:
            result = self.start_task(task['id'])
            if result and result['status'] == 'in_progress':
                self.log(f"Sukses, sedang memulai task {task['description']}", 'success')
            else:
                self.log(f"Tidak dapat mendapatkan info task {task['description']}", 'error')

        completed_tasks = [task for task in tasks_data['nodes'] if task['status'] == 'done']
        for task in completed_tasks:
            result = self.claim_task(task['id'])
            if result and 'claimed' in result:
                virt_money = result['claimed']['virt_money']
                virt_points = result['claimed']['virt_points']
                self.log(f"Task {task['description']} selesai sukses | Hadiah {virt_money} USD | {virt_points} VT", 'success')
            else:
                self.log(f"Gagal klaim hadiah  {task['description']}", 'error')

    def main(self):
        data_file = os.path.join(os.path.dirname(__file__), 'data.txt')
        with open(data_file, 'r', encoding='utf-8') as f:
            data = [line.strip() for line in f if line.strip()]

        while True:
            for i, init_data in enumerate(data):
                user_data = json.loads(urllib.parse.unquote(init_data.split('user=')[1].split('&')[0]))
                user_id = user_data['id']
                first_name = user_data['first_name']

                print(f"========== Account {i + 1} | {Fore.GREEN}{first_name} ==========")
                login_result = self.login_new_api(init_data)
                if login_result['success']:
                    self.log('Login Sukses!', 'success')
                    self.log(f"Nama : {login_result['data']['name']}")
                    self.log(f"Saldo USD : {login_result['data']['balances']['virt_money']}")
                    self.log(f"Saldo VT : {login_result['data']['balances']['virt_points']}")
                    self.log(f"Refferal: {login_result['data']['frens']['count']}/{login_result['data']['frens']['max']}")
                    
                    self.handle_autotrade()
                    self.play_tapping_game()
                    self.manage_tasks()
                else:
                    self.log(f"Login Gagal! {login_result['error']}", 'error')

                time.sleep(1)

            self.countdown(5)

if __name__ == "__main__":
    VooiDC.display_banner()
    client = VooiDC()
    try:
        client.main()
    except Exception as e:
        client.log(str(e), 'error')
        exit(1)
