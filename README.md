# Web-Shop
Проект интернет-магазина, разработанного на Django

## Функционал
1. Главная страница
- Отображение карточек товаров;
- Информация о товаре (название, цена, характеристики);
- Кнопка "Купить"

2. Страница контактов
- Контактная информация (адрес, телефон, email);
- Форма обратной связи (имя, email, сообщение);
- Обработка POST-запросов;
- Вывод сообщения об успешной отправке

## Установка
```bash
git clone https://github.com/Sofya-Ageeva/WebShop.git
cd WebShop
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver