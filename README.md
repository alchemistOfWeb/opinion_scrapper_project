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
* [3. Описание API и функционала приложения](#api_description)
    * [Регистрация и вход](#auth)
    * [Пользователи](#users)
    * [Доски](#boards)
    * [Задачи](#tasks)
    * [Теги для задач](#tasktags)
    * [Списки задач](#todolists)


## 1. Формулировка тз:
<a name="task_description"></a> 
За основу были взяты принципы работы kanban доски Trello

### Общие требования: 

* [x] REST API
* [x] Django, drf

* [x] Пользователь может создавать свои записи (в зависимости от задания), просматривать и удалять; просмотр доступен для списка записей и для каждой записи отдельно
* [x] Авторизация/аутентификация: 
    * [x] пользователь может регистрироваться в приложении (создание аккаунта)
    * [x] аутентификация (получение токена)
    * [x] выход из аккаунта (реализовано удаление токена из бд)
* [x] Ролевая модель(в данном случае встроенная в django): пользователи делятся на обычных и администраторов 
    * [x] зарегистрироваться в качестве администратора нельзя, можно только задать права вручную
    * [x] администратор может просматривать/редактировать/удалять любые записи любого пользователя
    * [x] администратор может создавать/удалять/блокировать пользователей.



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
git clone https://github.com/alchemistOfWeb/kanban_board_bkend.git
cd kanban_board_bkend
python -m venv venv
source <venv>/bin/activate # if u use linux
venv\Scripts\activate # if u use windows platform
pip install -r requirements.txt
```

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

Затем вы можете заимпортировать базу данных созданную мной с помощью средств джанго.
Для этого исполните следующую команду в терминале из директории `kanban_board_project/`:
```bash
python manage.py loaddata db.json
```

Также в таком случае вам не придётся создавать суперюзера, те. вы можете пропустить шаги 4 и 6.
Вот имя и пароль для доступа к админке
```txt
username: nikita
password: nikita
```

### 4 Миграции
<a name="migrations"></a> 

> Пропустите этот шаг, если вы выполнили django-миграцию бд (см. шаг 3)

Сделайте миграции в вашу бд
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Предварительный парсинг всех продуктов 
<a name="scrap_sitemap"></a> 

из каталога с `manage.py` выполните следующую команду
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