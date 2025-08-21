import time
import json
from playwright.sync_api import sync_playwright

# URL-адрес, который будет использоваться для скроллинга и скрапинга.
URL = "https://ttg.club/bestiary"


def scroll_with_keyboard(page):
    """
    Прокрутка до конца страницы с помощью нажатия клавиши "End".
    """
    page.keyboard.press("End")
    time.sleep(2)  # Задержка для загрузки контента


def scrape_cards(page):
    """
    Находит все карточки монстров на странице и извлекает из них данные.

    :param page: Объект страницы Playwright.
    :return: Список словарей с данными монстров.
    """
    print("\nНачало скрапинга карточек...")

    # Находим все элементы с классом 'link-item'.
    monster_cards = page.locator('.link-item').all()
    monsters_data = []

    # Проходим по каждой найденной карточке.
    for card in monster_cards:
        try:
            # Извлекаем имя, объединяя русское и английское названия.
            name_ru = card.locator('.link-item__name--rus').text_content().strip()
            name_en = card.locator('.link-item__name--eng').text_content().strip()

            # Извлекаем тип монстра.
            type_text = card.locator('.link-item__type').text_content().strip()

            # Извлекаем рейтинг сложности.
            cr = card.locator('.link-item__rating').text_content().strip()

            # Сохраняем данные в словарь.
            monsters_data.append({
                "name_ru": name_ru,
                "name_en": name_en,
                "challenge_rating": cr,
                "type": type_text
            })
        except Exception as e:
            # Обработка ошибок, если элемент не найден.
            print(f"Не удалось извлечь данные для одной из карточек: {e}")
            continue

    return monsters_data


def main():
    """
    Основная функция для выполнения автоматизации.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url=URL, wait_until="load")
        print(f"Заголовок страницы: {page.title()}")
        page.mouse.click(500, 0)

        # Первый скрапинг сразу после загрузки страницы
        scraped_data_initial = scrape_cards(page)
        print(f"Собрано {len(scraped_data_initial)} карточек на старте.")

        for i in range(1, 20):
            scroll_with_keyboard(page)
            print(f"Скролл #{i}")

        time.sleep(2)

        # Второй скрапинг после скроллинга
        scraped_data_final = scrape_cards(page)
        print(f"Собрано {len(scraped_data_final)} карточек после скроллинга.")

        # Объединение двух списков и удаление дубликатов
        # Используем set() для уникальности, т.к. на старте и в конце
        # могут быть одни и те же карточки.
        all_monsters = {json.dumps(d, sort_keys=True) for d in scraped_data_initial}
        all_monsters.update({json.dumps(d, sort_keys=True) for d in scraped_data_final})
        scraped_data = [json.loads(s) for s in all_monsters]

        with open('monsters.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=4)

        print("Данные успешно сохранены в monsters.json")

        # Вывод количества собранных карточек.
        print(f"\nВсего собрано {len(scraped_data)} уникальных карточек.")

        # Вывод первых 5 собранных данных для примера.
        if scraped_data:
            print("Первые 5 собранных карточек:")
            for item in scraped_data[:5]:
                print(item)
        browser.close()


if __name__ == "__main__":
    main()

