import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

url = 'https://www.divan.ru/krasnodar/category/promo-neshytochnaya?in_stock=1&categories%5B%5D=2210'


def parse_page(driver):
    data = []
    try:
        items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'lsooF'))
        )
    except TimeoutException:
        print("Таймаут при загрузке товаров")
        return data

    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text
            price = item.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU').text
            link = item.find_element(By.CSS_SELECTOR, 'link[itemprop="url"]').get_attribute('href')

            try:
                discount = item.find_element(By.CSS_SELECTOR, 'div.ui-OQy8X').text
            except NoSuchElementException:
                discount = "0%"  # Если скидки нет

            data.append([name, price, discount, link])

        except Exception as e:
            print(f'Ошибка парсинга товара: {e}')
            continue

    return data


def main():
    driver = webdriver.Firefox()
    try:
        driver.get(url)
        data = parse_page(driver)

        if data:
            with open('data.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Название товара', 'Цена по акции', 'Размер скидки, %', 'Ссылка на страницу товара'])
                writer.writerows(data)
            print(f"Успешно сохранено {len(data)} товаров")
        else:
            print('Данных для записи нет')

    finally:
        driver.quit()


if __name__ == "__main__":
    main()