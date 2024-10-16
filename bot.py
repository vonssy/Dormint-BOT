import requests
import json
import os
import urllib.parse
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
            'Host': 'api-new.dormint.io',
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
    
    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            first_name = user_data['first_name']
            return first_name
        else:
            raise ValueError("User data not found in query.")
        
    def auth(self, query: str, retries=5, delay=3):
        url = f'https://api-new.dormint.io/api/auth/telegram/verify?{query}'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
                
    def farming_status(self, token: str, retries=5, delay=3):
        url = 'https://api-new.dormint.io/tg/farming/status'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def start_farming(self, token: str, retries=5, delay=3):
        url = 'https://api-new.dormint.io/tg/farming/start'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_farming(self, token: str, retries=5, delay=3):
        url = 'https://api-new.dormint.io/tg/farming/claimed'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def invited_frens(self, token: str, retries=5, delay=3):
        url = 'https://api-new.dormint.io/tg/frens/invited'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_frens(self, token: str, claim_token: str, retries=5, delay=3):
        url = 'https://api-new.dormint.io/tg/frens/claimed'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def quests_list(self, token: str, retries=5, delay=3):
        url = 'https://api-new.dormint.io/tg/quests/list'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
    
    def start_quests(self, token: str, quest_id: str, retries=5, delay=3):
        url = 'https://api-new.dormint.io/tg/quests/start'
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
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
    
    def process_query(self, query: str):

        account = self.load_data(query)

        token = self.auth(query)
        if not token or token is None:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {account} {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}]{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} [ Token is None ] {Style.RESET_ALL}"
            )

        if token:
            farming = self.farming_status(token)
            if farming:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {farming['sleepcoin_balance']:.1f} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}                          "
                )

                frens = self.invited_frens(token)
                if frens:
                    for fren in frens:
                        if fren:
                            claim_token = fren['claim_secret']

                            if fren['balance'] != 0:
                                claim = self.claim_frens(token, claim_token)
                                if claim:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {fren['name']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {fren['balance']:.1f} {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}                          "
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Frens{Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}                          "
                                    )

                farming_left = farming['farming_left']
                farming_left_seconds = float(farming_left)
                farming_end_time = datetime.now().astimezone(wib) + timedelta(seconds=farming_left_seconds)

                claim = self.claim_farming(token)
                if claim:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Claimed{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {farming['farming_value']:.1f} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}                          "
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Already Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {farming_end_time.strftime('%x %X %Z')} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}                          "
                    )

                start = self.start_farming(token)
                if start:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT} Started{Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}                          "
                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Farming{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Already Started {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}                          "
                    )
         
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Failed to Get Farming Status ]{Style.RESET_ALL}                          ")

            quests = self.quests_list(token)
            if quests:
                for quest in quests:

                    if quest['status'] == 'quest_not_completed':
                        quest_id = quest['quest_id']
                        title = quest['name']
                        reward = quest['reward']

                        start = self.start_quests(token, quest_id)
                        if start:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {reward} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}Sleep Coins ]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}                          "
                            )
                        quests = self.quests_list(token)
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Failed to Get Quests List ]{Style.RESET_ALL}                          ")

        else:
            self.log(f"{Fore.RED+Style.BRIGHT}[ No token found for account: {account} ]{Style.RESET_ALL}                          ")


    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")
                        time.sleep(5)

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
