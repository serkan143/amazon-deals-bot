import requests
from bs4 import BeautifulSoup
import telebot
import time
import os

# Telegram bot token ve kullanıcı kimliği
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
bot = telebot.TeleBot(bot_token)

# Amazon fırsatlar sayfası URL'si
url = 'https://www.amazon.com.tr/deals'

def fetch_deals():
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    deals = []

    for deal in soup.find_all('div', class_='dealContainer'):
        title = deal.find('span', class_='dealTitle').get_text(strip=True)
        original_price = deal.find('span', class_='originalPrice').get_text(strip=True)
        discount_price = deal.find('span', class_='dealPrice').get_text(strip=True)
        image_url = deal.find('img', class_='dealImage')['src']
        
        deals.append({
            'title': title,
            'original_price': original_price,
            'discount_price': discount_price,
            'image_url': image_url
        })
    
    return deals

def send_deals(deals):
    for deal in deals:
        message = f"Ürün: {deal['title']}\nÖnceki Fiyat: {deal['original_price']}\nİndirimli Fiyat: {deal['discount_price']}"
        bot.send_photo(chat_id, deal['image_url'], caption=message)

def main():
    while True:
        deals = fetch_deals()
        if deals:
            send_deals(deals)
        else:
            print("No deals found.")
        time.sleep(300)  # 5 dakika bekle

if __name__ == "__main__":
    main()
