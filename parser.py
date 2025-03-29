import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.divan.ru/krasnodar/category/promo-neshytochnaya?in_stock=1&categories%5B%5D=2210'
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 10)
sale = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'lsooF')))
data = []

for item in sale:
    try:
        name = item.find_element(By.CSS_SELECTOR,'span[itemprop="name"]').text
        price = item.find_element(By.CSS_SELECTOR,'span.ui-LD-ZU').text
        discount = item.find_element(By.CSS_SELECTOR,'div.ui-OQy8X').text
        link = item.find_element(By.CSS_SELECTOR,'link[itemprop="url"]').get_attribute('href')
    except Exception as e:
        print (f'Ошибка парсинга: {e}')
        continue
    data.append([name, price, discount, link])
driver.quit()

if data:
    with open('data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Название товара', 'Цена по акции', 'Размер скидки, %', 'Ссылка на страницу товара'])
        writer.writerows(data)
else:
    print('Данных для записи нет')
