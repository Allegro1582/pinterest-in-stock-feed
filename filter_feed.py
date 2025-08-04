import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Конфигурация
FEED_URL = "https://exult.ua/marketplace-integration/google-feed?langId=3"
OUTPUT_FILE = "pinterest_in_stock_feed.xml"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

try:
    # Загружаем фид с заголовками
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(FEED_URL, headers=headers, timeout=30)
    response.raise_for_status()

    # Парсим XML
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        raise ValueError(f"Ошибка парсинга XML: {str(e)}")

    # Namespace
    ns = {'g': 'http://base.google.com/ns/1.0'}

    # Создаем новый фид
    new_root = ET.Element('rss', version='2.0')
    channel = ET.SubElement(new_root, 'channel')
    ET.SubElement(channel, 'title').text = "Pinterest Feed (In Stock)"
    ET.SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Фильтруем товары в наличии
    in_stock_count = 0
    for item in root.findall('.//item'):
        availability = item.find('g:availability', ns)
        if availability is not None and availability.text.lower() == 'in stock':
            channel.append(item)
            in_stock_count += 1

    # Сохраняем результат (ОДИН раз)
    ET.ElementTree(new_root).write(OUTPUT_FILE, encoding='utf-8', xml_declaration=True)
    print(f"Успешно! Товаров в наличии: {in_stock_count}. Файл: {OUTPUT_FILE}")

except Exception as e:
    print(f"Критическая ошибка: {str(e)}", file=sys.stderr)
    sys.exit(1)
