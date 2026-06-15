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
1. Клонирование репозитория
```
git clone https://github.com/Sofya-Ageeva/WebShop.git
cd WebShop
```
2. Создание и активация виртуального окружения
 2.1. Для macOS/Linux
```
python -m venv venv
source venv/bin/activate
```
 2.2. Для Windows
```
python -m venv venv
venv/Scripts/activate
```
3. Установка зависимостей
```
pip install -r requirements.txt
```
4. Настройка уязвимых данных
```
cp .env.template .env
```
Отредактируйте файл .env
5. Создание базы данных
```
psql -U postgres -c "CREATE DATABASE webshop_db;"
```
6. Миграция и запуск приложения
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```