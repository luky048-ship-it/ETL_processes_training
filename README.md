# ETL_processes_training
This repository is for teaching ETL processes in the HSE Master's programme in Data Engineering
# airflow_training
P.S: Данные для проверки расположенны в папке Airflow/dags (сам DAG, 2 csv-фаила с таблицами в "плоской" форме)
## Описание проекта
Реализация базового ETL-процесса для сбора и обработки разнородных данных (JSON, XML). Пайплайн автоматизирован с помощью Apache Airflow и развернут в Docker-инфраструктуре.
## Технологический стек
* **Оркестрация:** Apache Airflow 2.9.3
* **База данных:** PostgreSQL 14
* **Язык обработки:** Python 3.11 (библиотеки: Pandas, SQLAlchemy, requests, lxml)
* **Инфраструктура:** Docker, Docker-compose
* **Аналитика:** Jupyter Lab

## Логика пайплайна

### 1. Extract & Transform
Пайплайн состоит из двух основных задач, выполняемых PythonOperator:

* **Обработка JSON (`pets_data`):** Сбор данных о питомцах через API. Реализована очистка текстовых полей от HTML-тегов с помощью регулярных выражений (`re`) для нормализации строковых данных.
* **Обработка XML (`nutrition_data`):** Парсинг сложной структуры XML с динамическим распределением атрибутов (витамины, минералы) в плоскую таблицу. 

### 2. Load
Данные загружаются в PostgreSQL. Использован метод `if_exists='replace'` через SQLAlchemy engine. 
* **Хост базы:** `postgres` (внутренняя сеть Docker).
* **Таблицы:** `pets`, `nutrition`.

## Как запустить
1. Склонировать репозиторий.
2. Поднять окружение: `docker-compose up -d`.
3. Перейти в UI Airflow (localhost:8080) и запустить DAG `data_sources_transform`.
4. Проверить результат в базе можно через терминал:
   `docker exec -it de-postgres psql -U airflow -d airflow`
   или в Jupiter (localhost:8888) через сохраненый код в SQL_conclusion.ipynb
