import xml.etree.ElementTree as ET
import datetime

# Укажите имя вашего исходного файла (если он в облаке, нужна ссылка)
input_file = "google_merchant_feed.xml"
output_file = "pinterest_in_stock_feed.xml"

# Загружаем XML
tree = ET.parse(input_file)
root = tree.getroot()

# Пространство имён Google Merchant (если есть)
ns = {'g': 'http://base.google.com/ns/1.0'}

# Создаём новый фид
new_root = ET.Element('rss', version='2.0')
channel = ET.SubElement(new_root, 'channel')

# Заголовок и дата
title = ET.SubElement(channel, 'title')
title.text = "Pinterest Feed (In Stock Only)"
last_build_date = ET.SubElement(channel, 'lastBuildDate')
last_build_date.text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# Фильтруем товары в наличии
for item in root.findall('.//item'):
    availability = item.find('g:availability', ns)
    if availability is not None and availability.text.lower() == 'in stock':
        channel.append(item)  # Копируем в новый фид

# Сохраняем
new_tree = ET.ElementTree(new_root)
new_tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"Фид с товарами в наличии сохранён в {output_file}")
