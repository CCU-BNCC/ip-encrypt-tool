#!/usr/bin/env python3
import os
import threading
import requests
from cryptography.fernet import Fernet
from time import sleep

# =========[ Banner ]=========
def banner():
    os.system("clear")
    print("\033[1;31m")
    print("     ██████╗")
    print("    ██╔═══██╗  IP Encrypt & Stress Test Tool")
    print("    ███████╔╝  Created by A")
    print("    ██╔═══╝")
    print("    ██║")
    print("    ╚═╝")
    print("\033[0m")

# =========[ Key Generator ]=========
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# =========[ Key Loader ]=========
def load_key():
    return open("secret.key", "rb").read()

# =========[ Encrypt Data ]=========
def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# =========[ Threaded Request ]=========
def send_request(target_url):
    while True:
        try:
            response = requests.get(target_url)
            print(f"\033[1;32m[✓] Status: {response.status_code}\033[0m")
        except requests.exceptions.RequestException as e:
            print(f"\033[1;31m[!] Error: {e}\033[0m")
        sleep(0.2)

# =========[ Main Program ]=========
def main():
    banner()

    if not os.path.exists("secret.key"):
        print("\033[1;33m[*] Generating secret key...\033[0m")
        generate_key()

    target_ip = input("\033[1;36m[>] Enter the target IP address (e.g., 127.0.0.1): \033[0m")

    if not target_ip:
        print("\033[1;31m[!] No IP entered. Exiting.\033[0m")
        return

    encrypted_ip = encrypt_data(target_ip)
    with open("saved_ip.txt", "wb") as f:
        f.write(encrypted_ip)

    print("\033[1;32m[✓] Encrypted IP saved to saved_ip.txt\033[0m")

    target_url = f"http://{target_ip}"
    print("\033[1;35m[*] Starting threads...\033[0m")

    thread_count = 1  # <- ১টি থ্রেড এখানে
    for i in range(thread_count):
        t = threading.Thread(target=send_request, args=(target_url,))
        t.daemon = True
        t.start()

    while True:
        sleep(1)

if __name__ == "__main__":
    main()
