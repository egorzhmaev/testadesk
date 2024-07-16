# Тестовое задание

## Установка 🔧

### 1. Настройка проекта
- Создайте виртуальное окружение и активируйте его.
- Установите зависимости из файла `requirements.txt`.
  ```shell
  pip install -r requirements.txt
  ```

### 2. Конфигурация среды
- Заполните env.dev необходимыми данными:
    ```
    SECRET_KEY='your secret key'
    DEBUG=1
    ALLOWED_HOSTS=127.0.0.1 localhost
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=
    ```

### 3. Запуск приложения
- Приложение будет доступно по адресу `http://127.0.0.1:8000`.
  ```shell
  python manage.py runserver
  ```
- Запуск приложения в Докер
  ```shell
  docker compose -f docker-compose.dev.yml build  
  docker compose -f docker-compose.dev.yml up
  ```

## Тестирование
- Заполните базу данных
- С помощью команды ниже создайте дамп базы данных
```shell 
python -Xutf8 manage.py dumpdata -o db_test.json 
``` 
- Запустите тесты с помощью команды `python manage.py tests`.

## Эндпоинты
- Создание счёта
```
POST /accounts
Параметры запроса:
name — название счета
```
- Получение списка счетов
```
GET /accounts
Параметры запроса: —
Ответ: список объектов с полями
id — идентификатор счета
name — название счета
balance — текущий баланс счета (сумма всех операций на счету)
```
- Создание операции
```
POST /transactions
Параметры запроса:
account_id — идентификатор счета, к которому относится операция
date — дата операции
amount — сумма операции (положительная для поступлений, отрицательная для списаний)
Ответ: объект с полями
id — идентификатор операции
account_id — идентификатор счета
date — дата операции
amount — сумма операции
```
- Удаление операции
```
DELETE /transactions/<id>
Параметры запроса: —
Ответ: —
```
- Получение списка операций
```
GET /transactions
Параметры запроса для фильтрации (все необязательные):
accounts — список id счетов, по которым нужно получить операции
date_from — с какой даты (включительно) нужно получить операции
date_to — до какой даты (включительно) нужно получить операции
amount_from — минимальная (включительно) сумма операции
amount_to — максимальная (включительно) сумма операции
Ответ: список объектов с полями
id — идентификатор операции
account_id — идентификатор счета
account_balance — баланс счета на момент совершения операции (сумма всех операций до текущей включительно в хронологическом порядке)
date — дата операции
amount — сумма операции
```
