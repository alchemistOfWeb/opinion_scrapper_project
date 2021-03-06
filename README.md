# Opinions scrapper
#### developed by Nikita Kuznetsov


* [1. Формулировка тз](#task_description)
* [2. Установка и настройка](#setup)
    * [1. Установка зависимостей](#dependences)
    * [2. Секретный ключ](#create_secret_key)
    * [3. Настройка базы данных](#setup_db)
    * [4. Миграции](#migrations)
    * [5. Предварительный парсинг всех продуктов](#scrap_sitemap)
    * [6. Для доступа к админке ](#admin_panel)
    * [7. Запуск тестового сервера](#test_server)
* [3. Описание функционала приложения](#description)
    * [Регистрация и вход](#auth)
    * [Пользователи](#users)
    * [Ссылки на все товары](#products)
    * [Список комментариев к товару](#opinions)


## 1. Формулировка тз:
<a name="task_description"></a> 


### Общие требования: 

* Написать парсер комментариев с сайта DNS-shop
* Пример карточки товара https://www.dns-shop.ru/product/e17da1b7ddc73333/mikrovolnovaa-pec-winia-kor-6607ww-belyj/opinion/

* [ ] Сложность - комментарии подгружаются, динамически, тот кто спарсит все + балл.
>> не успел, но для себя позже сделаю
* [x] Сложность небольная но есть - для начала нужно будет сделать карту сайта с карточками товаров(либо взять из сайтмеп).
>> Тк сайтмеп не нашёл - сделал таблицу в бд для хранения ссылок на все карточки.
* [x] Потом положить их в модельку где есть
    * [x] урлу карточки товара
    * [x] название товара
    * [x] кол-во комметариев
    * [x] звездочки
    * [x] автор
    * [x] источник
    * [x] срок использования
    * [x] достоинства
    * [x] недостатки
    * [x] текст комментария
* [x] И сделать простую Django админку(можно любую дургую), что бы можно было
    * [x] смотреть комментарии
    * [x] фильтровать по звездочкам
    * [x] источнику
    * [x] искать по тексту
    * [x]


<br><br>

---
---
---
---

<br>  

## 2. Установка и настройка
<a name="setup"></a> 

### 1 Установка зависимостей
<a name="dependences"></a> 

Для начала установите python.
Допустимы версии от 3.6 до 3.9


```bash
cd нужный каталог
git clone https://github.com/alchemistOfWeb/opinion_scrapper_project.git
cd opinion_scrapper_project
python -m venv venv
source <venv>/bin/activate # if u use linux
venv\Scripts\activate # if u use windows platform
pip install -r requirements.txt
```

Далее установите и настройте geckodriver (нужно для работы selenium).
скачать можно отсюда, выбрав архив подходящий под вашу ОС https://github.com/mozilla/geckodriver/releases. После скачивания, распакуйте
После его установки укажите путь в файле `opinion_scrapper/opinion_scrapper/settings.py` в переменную `GECKODRIVER_PATH`.


### 2 Секретный ключ
<a name="create_secret_key"></a> 

Для начала скопируйте файл .env.example и уберите строку `.example` из названия копии (оставьте только `.env`)

Создайте секретный ключ и добавьте в настройки соответствующими командами:
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key()) # скопируйте полученный командой ключ
>>> exit()
dotenv set SECRET_KEY 'getted_secret_key' # сюда нужно вставить полученный ключ
```

### 3 Настройка базы данных
<a name="setup_db"></a> 

Установите настройки для вашей бд в `.env` файле. Ниже приведён пример и названия параметров, которые можно использовать. 
```py
DB_NAME='opinion_scrapper'
DB_USER='admin'
DB_PASS='admin'
DB_HOST='127.0.0.1'
DB_PORT='5432'
```
По умолчанию используется движок `postgress`, для его изменения измените значение словаря `DATABASES` в `opinion_scrapper/settings.py`.
Посмотреть корректные названия движков для подключения к др. базам данных можно на https://docs.djangoproject.com/en/3.1/ref/databases/

### 4 Миграции
<a name="migrations"></a> 

Сделайте миграции в вашу бд
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Предварительный парсинг всех продуктов 
<a name="scrap_sitemap"></a> 

из каталога с `manage.py` выполните следующую команду. Будет выполняться несколько часов.
```bash
python manage.py scrape_products
```
затем следующую для скрапинга всех комментариев для этих товаров
```bash
python manage.py scrape_opinions
```


### 6 Для доступа к админке 
<a name="admin_panel"></a> 

> Пропустите этот шаг, если вы выполнили django-миграцию бд (см. шаг 3)

Создайте суперюзера для доступа к админке
```bash
python manage.py create superuser
name: ******* # придумайте, например admin
pas: ********** # придумайте, например admin
```

### 7 Запуск тестового сервера
<a name="test_server"></a> 

теперь можно запустить тестовый сервер
```bash
python manage.py runserver
```

## 3. Описание функционала приложения
<a name="description"></a> 

### регистрация/вход
<a name="auth"></a> 

Нового пользователя может создать только админ. Вход стандартный из коробки django


### пользователи
<a name="users"></a> 

Cтандартно из коробки django

### ссылки на все товары
<a name="products"></a>

Карта сайта с ссылками на все товары. Нужно для парсинга комментариев.
Написал изходя из предположения, что на сайт днс периодически будут добавлятся новые товары, а также новые категории товаров.

### список комментариев(отзывов) пользователей
<a name="opinions"></a>

Для каждого комментария спарсены все необходимые данные
