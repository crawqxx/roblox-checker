import requests
from colorama import Fore, Style
import itertools
import time
from tqdm import tqdm
import os

def validate_username(username, retries=3):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                code = data.get("code", -1)

                if code == 0:
                    tqdm.write(f"{Fore.GREEN}[AVAILABLE]{Style.RESET_ALL} {username}")
                    with open("available.txt", "a") as f:
                        f.write(username + "\n")
                else:
                    tqdm.write(f"{Fore.RED}[TAKEN]{Style.RESET_ALL} {username}")
                    with open("taken.txt", "a") as f:
                        f.write(username + "\n")
                return
            else:
                tqdm.write(f"{Fore.YELLOW}[HTTP ERROR {response.status_code}] {username}{Style.RESET_ALL}")
        except requests.RequestException as e:
            tqdm.write(f"{Fore.YELLOW}[NETWORK ERROR] {e} (Attempt {attempt + 1}){Style.RESET_ALL}")
            time.sleep(1)
    tqdm.write(f"{Fore.RED}[FAILED] {username} after retries{Style.RESET_ALL}")

def get_last_checked():
    files = ["available.txt", "taken.txt"]
    last = None
    for file in files:
        if os.path.exists(file):
            with open(file, "r") as f:
                lines = f.read().splitlines()
                if lines:
                    last = lines[-1]
    return last

def generate_username_sequence():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    combos = itertools.product(letters, repeat=4)
    for combo in combos:
        yield f"{combo[0]}_{combo[1]}{combo[2]}{combo[3]}"
        yield f"{combo[0]}{combo[1]}{combo[2]}_{combo[3]}"

def generate_usernames_and_check():
    total_usernames = 26 ** 4 * 2
    last_checked = get_last_checked()
    skipping = bool(last_checked)
    found_last = not skipping 

    with tqdm(total=total_usernames, desc="checking usernames", unit="user") as progress:
        for username in generate_username_sequence():
            if skipping and not found_last:
                if username == last_checked:
                    found_last = True
                progress.update(1)
                continue

            validate_username(username)
            progress.update(1)

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}starting username availability checker {Style.RESET_ALL}")
    generate_usernames_and_check()
