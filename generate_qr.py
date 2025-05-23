import os
from PIL import Image
import qrcode

# Настройки (можно изменять)
SETTINGS = {
    "input": {
        "kids_photos": "детские_фото",
        "links": "ссылки"
    },
    "output": {
        "folder": "готовые_фото",
        "qr_position": (0, 0),  # Отступ QR-кода от правого нижнего угла
        "qr_size": 125  # Размер стороны QR-кода (уменьшен)
    },
    "bitly": {
        "api_key": "d75c67f64c084b81b63c5104e98c36ba026d9911",
        "base_url": "https://api-ssl.bitly.com/v4/shorten"
    }
}

def find_files(base_folder, extension):
    return {os.path.splitext(f)[0]: os.path.join(base_folder, f) 
            for f in os.listdir(base_folder) if f.endswith(extension)}

def process_images():
    os.makedirs(SETTINGS['output']['folder'], exist_ok=True)
    
    # Собираем только нужные файлы
    kids = find_files(SETTINGS['input']['kids_photos'], '.jpg')
    links = find_files(SETTINGS['input']['links'], '.txt')
    
    for name in kids:
        try:
            # Проверяем наличие только ссылки
            if name not in links:
                print(f"Нет ссылки для {name}")
                continue
            
            # Загружаем данные
            kid_img_path = kids[name]
            with open(links[name], 'r', encoding='utf-8') as f:
                link = f.read().strip()
            
            # Генерируем QR-код
            qr = qrcode.QRCode(box_size=5)
            qr.add_data(link)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img = qr_img.resize((SETTINGS['output']['qr_size'],)*2)
            
            # Открываем исходное изображение
            kid_img = Image.open(kid_img_path)
            
            # Создаем копию изображения для добавления QR-кода
            final_img = kid_img.copy()
            
            # Вставляем QR-код
            qr_pos_x = final_img.width - qr_img.width - SETTINGS['output']['qr_position'][0]
            qr_pos_y = final_img.height - qr_img.height - SETTINGS['output']['qr_position'][1]
            final_img.paste(qr_img, (qr_pos_x, qr_pos_y))
            
            # Сохраняем результат
            output_path = os.path.join(SETTINGS['output']['folder'], f"{name}.jpg")
            final_img.save(output_path)
            print(f"Обработано: {name}")
        
        except Exception as e:
            print(f"Ошибка при обработке {name}: {str(e)}")

if __name__ == "__main__":
    process_images()