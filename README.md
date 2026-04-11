# ParserTest

A Playwright-based web scraper that collects the full D&D 5e monster bestiary from [ttg.club](https://ttg.club/bestiary). The scraper automates a browser session, progressively scrolls the lazy-loaded page, and saves all unique monster entries to a structured JSON file.

## What It Collects

For each monster card on the page, the scraper extracts:

| Field | Description |
|---|---|
| `name_ru` | Monster name in Russian |
| `name_en` | Monster name in English |
| `type` | Creature type (e.g. Beast, Undead, Dragon) |
| `challenge_rating` | Challenge rating (CR) |

Results are deduplicated and saved to `monsters.json`.

## How It Works

1. Opens a Chromium browser and navigates to the bestiary page
2. Takes an initial snapshot of loaded monster cards
3. Presses `End` 19 times with 2-second pauses to trigger lazy loading
4. Takes a second snapshot of all visible cards
5. Merges both snapshots, removes duplicates, and writes `monsters.json`

## Requirements

- Python 3.10+
- Playwright with Chromium

## Installation

```bash
git clone https://github.com/Nezdeshniy/ParserTest.git
cd ParserTest
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
python main.py
```

The browser window will open (non-headless). Output is printed to the terminal and results are saved to `monsters.json`.

**Example output:**

```
Заголовок страницы: Бестиарий | TTG.club
Начало скрапинга карточек...
Собрано 42 карточек на старте.
Скролл #1
...
Всего собрано 387 уникальных карточек.
Данные успешно сохранены в monsters.json
```

## Output Format

```json
[
    {
        "name_ru": "Гоблин",
        "name_en": "Goblin",
        "challenge_rating": "1/4",
        "type": "Гуманоид"
    }
]
```

## Dependencies

| Package | Purpose |
|---|---|
| `playwright` | Browser automation |
| `greenlet` | Playwright async support |
