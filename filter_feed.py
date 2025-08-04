import requests
import xml.etree.ElementTree as ET

# 1. Загружаем исходный фид
feed_url = "https://exult.ua/marketplace-integration/google-feed?langId=3"
response = requests.get(feed_url)
root = ET.fromstring(response.content)

# 2. Фильтруем только in stock (сохраняем ВСЁ остальное)
ns = {'g': 'http://base.google.com/ns/1.0'}
for item in root.findall('.//item'):
    availability = item.find('g:availability', ns)
    if availability is None or availability.text.lower() != 'in stock':
        root.find('.//channel').remove(item)

# 3. Сохраняем КАК ЕСТЬ (с оригинальными тегами и структурой)
tree = ET.ElementTree(root)
tree.write("pinterest_in_stock_feed.xml", encoding='utf-8', xml_declaration=True)
