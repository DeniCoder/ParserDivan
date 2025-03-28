import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

base_url = 'https://www.divan.ru'
target_url = 'https://www.divan.ru/krasnodar/category/promo-neshytochnaya?in_stock=1&categories%5B%5D=2210'


def fetch_page(url):
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        return None


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='lsooF')
    data = []

    for item in items:
        try:
            name = item.find('span', itemprop='name').get_text(strip=True)
            price = item.find('span', class_='ui-LD-ZU').get_text(strip=True)
            discount = item.find('div', class_='ui-OQy8X').get_text(strip=True) if item.find('div',
                                                                                             class_='ui-OQy8X') else "0%"
            rel_link = item.find('link', itemprop='url')['href']
            link = urljoin(base_url, rel_link)

            data.append([name, price, discount, link])
        except Exception as e:
            print(f"Ошибка парсинга элемента: {e}")
            continue

    return data


def main():
    print("Начало парсинга...")
    html = fetch_page(target_url)

    if not html:
        print("Не удалось загрузить страницу")
        return

    data = parse_page(html)

    if data:
        with open('data_bs4.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Название товара', 'Цена по акции', 'Размер скидки, %', 'Ссылка на страницу товара'])
            writer.writerows(data)
        print(f"Успешно сохранено {len(data)} товаров")
    else:
        print("Не найдено данных для сохранения")


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Время выполнения: {time.time() - start_time:.2f} секунд")