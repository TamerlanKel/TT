import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import time


def get_animals_count():
    base_url = "https://ru.wikipedia.org"
    url = base_url + "/wiki/Категория:Животные_по_алфавиту"
    letter_counts = defaultdict(int)

    while True:
        try:
            print(f"Обрабатываю страницу: {url}")
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим блок с категориями
            category_block = soup.find('div', class_='mw-category-columns')
            if not category_block:
                print("Не найден блок с категориями")
                break

            # Обрабатываем всех животных на странице
            animal_links = category_block.find_all('a')
            for link in animal_links:
                name = link.text.strip()
                if name:
                    first_letter = name[0].upper()
                    if 'А' <= first_letter <= 'Я':
                        letter_counts[first_letter] += 1

            # Ищем ссылку на следующую страницу
            next_page = soup.find('a', string='Следующая страница')
            if not next_page:
                print("Достигнут конец списка")
                break

            url = base_url + next_page['href']
            time.sleep(1)  # Задержка между запросами

        except Exception as e:
            print(f"Ошибка: {e}")
            break

    return letter_counts


def save_to_csv(counts):
    with open('../beasts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Записываем заголовок
        writer.writerow(['Буква', 'Количество'])
        # Сортируем по алфавиту и записываем данные
        for letter in sorted(counts.keys()):
            writer.writerow([letter, counts[letter]])


if __name__ == "__main__":
    print("Начинаю сбор данных...")
    counts = get_animals_count()
    save_to_csv(counts)
    print("Данные успешно сохранены в beasts.csv")
    print("Результат:")
    for letter, count in sorted(counts.items()):
        print(f"{letter}: {count}")