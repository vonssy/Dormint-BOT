import requests
import json
import os
from urllib.parse import parse_qs, unquote
from colorama import *
from datetime import datetime, timedelta
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class Dormint:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'gate.api-dormint.com',
            'Origin': 'https://web.dormint.io',
            'Pragma': 'no-cache',
            'Referer': 'https://web.dormint.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Dormint - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def extract_user_data(self, query: str) -> str:
        parsed_query = parse_qs(query)
        user_data = parsed_query.get('user', [None])[0]

        if user_data:
            user_json = json.loads(unquote(user_data))
            return str(user_json.get('first_name', 'Unknown'))
        return 'Unknown'

    def load_tokens(self):
        try:
            if not os.path.exists('tokens.json'):
                return {"accounts": []}

            with open('tokens.json', 'r') as file:
                data = json.load(file)
                if "accounts" not in data:
                    return {"accounts": []}
                return data
        except json.JSONDecodeError:
            return {"accounts": []}

    def save_tokens(self, tokens):
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file, indent=4)

    def generate_tokens(self, queries: list):
        tokens_data = self.load_tokens()
        accounts = tokens_data["accounts"]

        for idx, query in enumerate(queries):
            account_name = self.extract_user_data(query)

            existing_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)

            if not existing_account:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Token Is None{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Generating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)

                token = self.auth(query)
                if token:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )
                    accounts.insert(idx, {"first_name": account_name, "token": token})
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)

        self.save_tokens({"accounts": accounts})

    def renew_token(self, account_name):
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])
        
        account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        
        if account and "token" in account:
            token = account["token"]
            if not self.farming_status(token):
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Token Isn't Valid{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Regenerating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)
                
                accounts = [acc for acc in accounts if acc["first_name"] != account_name]
                
                query = next((query for query in self.load_queries() if self.extract_user_data(query) == account_name), None)
                if query:
                    new_token = self.auth(query)
                    if new_token:
                        accounts.append({"first_name": account_name, "token": new_token})
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Query Is None. Skipping {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
        
        self.save_tokens({"accounts": accounts})

    def load_queries(self):
        with open('query.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
        
    def auth(self, query: str, retries=5, delay=3):
        url = f'https://gate.api-dormint.com/api/auth/telegram/verify?{query}'
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                if response.status_code == 200:
                    result = response.text.strip('"')
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def farming_status(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/farming/status'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
                
    def invited_frens(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/frens/invited'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result['frens']
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_frens(self, token: str, claim_token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/frens/claimed'
        data = json.dumps({'auth_token': token, 'claim_token': claim_token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def start_farming(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/farming/start'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_farming(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/farming/claimed'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
                
    def lootboxes_status(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/lootboxes/status'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
                
    def buy_lootboxes(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/lootboxes/buy/sleepcoins'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
                
    def open_lootboxes(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/lootboxes/open'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result['lootboxPrize']
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def quests_list(self, token: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/quests/list'
        data = json.dumps({'auth_token': token})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result:
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
    
    def start_quests(self, token: str, quest_id: str, retries=5, delay=3):
        url = 'https://gate.api-dormint.com/tg/quests/start'
        data = json.dumps({'auth_token': token, 'quest_id': quest_id})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if result['status'] == 'ok':
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError, json.JSONDecodeError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
    
    def process_query(self, query: str):
        account_name = self.extract_user_data(query)
    
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])

        exist_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        if not exist_account:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT}Token Not Found in tokens.json{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} ]{Style.RESET_ALL}"
            )
            return
        
        if exist_account and "token" in exist_account:
            token = exist_account["token"]

            farming = self.farming_status(token)
            if not farming:
                self.renew_token(account_name)
                tokens_data = self.load_tokens()
                new_account = next((acc for acc in tokens_data["accounts"] if acc["first_name"] == account_name), None)
                
                if new_account and "token" in new_account:
                    new_token = new_account["token"] 
                    farming = self.farming_status(new_token)

            if farming:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {farming['sleepcoin_balance']:.1f} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}"
                )

                frens = self.invited_frens(new_token if 'new_token' in locals() else token)
                if frens:
                    for fren in frens:
                        if fren:
                            claim_token = fren['claim_secret']

                            if fren['balance'] != 0:
                                claim = self.claim_frens(new_token if 'new_token' in locals() else token, claim_token)
                                if claim:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {fren['name']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}IS Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {fren['balance']:.1f} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )

                farming_left = farming['farming_left']
                farming_left_seconds = float(farming_left)
                farming_end_time = datetime.now().astimezone(wib) + timedelta(seconds=farming_left_seconds)

                claim = self.claim_farming(new_token if 'new_token' in locals() else token)
                if claim:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Claimed{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {farming['farming_value']:.1f} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {farming_end_time.strftime('%x %X %Z')} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

                start = self.start_farming(new_token if 'new_token' in locals() else token)
                if start:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Is Started{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Is Already Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

                lootboxes = self.lootboxes_status(new_token if 'new_token' in locals() else token)
                if lootboxes:
                    balance = lootboxes['sleepcoinBalance']
                    price = 500
                    lootboxes_count = lootboxes['lootboxCount']
                    lootboxes_left = lootboxes['lootboxBySleepcoinsLeft']

                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Lootboxes{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} Have {lootboxes_count} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Can Buy{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {lootboxes_left} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

                    if balance >= price:
                        while lootboxes_left > 0:
                            buy = self.buy_lootboxes(new_token if 'new_token' in locals() else token)
                            if buy:
                                balance = buy['sleepcoinBalance']
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Lootboxes{Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} Was Successfully Purchased{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}] [ You Have{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {buy['lootboxCount']} Lootboxes {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                break

                        if lootboxes_left == 0:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Lootboxes{Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT} Not Available For Purchase {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )

                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Lootboxes{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Not Enough Sleepcoins For Purchase {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                    lootboxes_count = self.lootboxes_status(new_token if 'new_token' in locals() else token)['lootboxCount']
                    while lootboxes_count > 0:
                        open = self.open_lootboxes(new_token if 'new_token' in locals() else token)
                        if open:
                            lootboxes_count = self.lootboxes_status(new_token if 'new_token' in locals() else token)['lootboxCount']
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Lootboxes{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} Is Opened {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {open['amount']} {open['prize_type']} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ You Have{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {lootboxes_count} Left {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            break

                    if lootboxes_count == 0:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Lootboxes{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Not Available For Open {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Lootboxes{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

                quests = self.quests_list(new_token if 'new_token' in locals() else token)
                if quests:
                    for quest in quests:

                        if quest['status'] == 'quest_not_completed':
                            quest_id = quest['quest_id']
                            title = quest['name']
                            reward = quest['reward']

                            start = self.start_quests(new_token if 'new_token' in locals() else token, quest_id)
                            if start:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {title} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {reward} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {title} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Completed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            quests = self.quests_list(new_token if 'new_token' in locals() else token)
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )

    def main(self):
        self.clear_terminal()
        try:
            queries = self.load_queries()
            self.generate_tokens(queries)

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Dormint - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    dormint = Dormint()
    dormint.main()
