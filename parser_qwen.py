import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка WebDriver
options = Options()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)

driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(300)  # Увеличенный таймаут

try:
    # Загрузка страницы
    url = 'https://www.divan.ru/krasnodar/category/promo-neshytochnaya?in_stock=1&categories%5B%5D=2210'
    driver.get(url)

    # Ожидание загрузки элементов
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lsooF')))

    # Поиск товаров
    sale = driver.find_elements(By.CLASS_NAME, 'lsooF')
    data = []

    for item in sale:
        try:
            name = item.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
            price = item.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU').text
            discount_element = item.find_elements(By.CSS_SELECTOR, 'div.ui-OQy8X')
            discount = discount_element[0].text if discount_element else 'Нет скидки'
            link = item.find_element(By.CSS_SELECTOR, 'link[itemprop="url"]').get_attribute('href')
        except Exception as e:
            print(f'Ошибка парсинга: {e}')
            continue
        data.append([name, price, discount, link])

    # Запись данных в CSV
    if data:
        with open('data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Название товара', 'Цена по акции', 'Размер скидки, %', 'Ссылка на страницу товара'])
            writer.writerows(data)
    else:
        print("Нет данных для записи.")

finally:
    driver.quit()