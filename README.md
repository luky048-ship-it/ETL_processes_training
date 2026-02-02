# ETL Processes Training (HSE Master's Programme)

Этот репозиторий содержит комплекс выполненных работ по автоматизации сбора, трансформации и загрузки данных (ETL). Проект реализован в рамках магистерской программы Инженерия данных и охватывает сценарии работы с API, XML-файлами, а также IoT-данными.

## Технологический стек
* Оркестрация: Apache Airflow 2.9.3 (контейнеризированный запуск)
* Хранилище: PostgreSQL 14
* Анализ данных: Jupyter Lab (Python 3.11, Pandas, SQLAlchemy, NumPy)
* Инфраструктура: Docker, Docker-compose, nvim

## Структура проекта
```
.
├── README.md
└── airflow_training
    ├── docker-compose.yml
    ├── airflow
    │   ├── dags
    │   │   ├── DAG_operator.py
    │   │   ├── homework2_etl.py
    │   │   ├── *.csv
    │   │   └── screenshot
    │   └── logs
    ├── init
    │   └── init.sql
    └── jupyter
        └── notebooks
            ├── SQL_conclusion.ipynb
            └── read_csv.ipynb
```
## Описание реализованных пайплайнов

### 1. Обработка API и XML (Задание 1)
DAG: data_sources_transform
* Extract: Автоматический сбор данных о питомцах (JSON через API) и разбор данных о нутриентах (XML).
* Transform: Нормализация вложенных структур XML в плоские таблицы и очистка JSON-полей от HTML-разметки с помощью регулярных выражений.
* Load: Загрузка в PostgreSQL (таблицы pets, nutrition).

### 2. Трансформация и загрузка данных IoT (Задания 2, 3, 4)
DAG: weather_etl_final_step
* Transformation:
    * Фильтрация замеров внутри помещений (In).
    * Приведение временных меток к формату date.
    * Очистка аномалий: Удаление температурных выбросов за пределами 5-го и 95-го процентилей.
* Analytics: Вычисление 5 самых жарких и холодных дней за период.
* Loading Strategies:
    * Full Load: Полная перезагрузка исторического набора данных в таблицу weather_full.
    * Incremental Load: Изоляция и загрузка данных только за последние 3 дня в weather_incremental.

## Результаты выполнения
Результаты работы пайплайнов и подтверждающие скриншоты расположены в папке airflow_training/airflow/dags/screenshot/:

1. Общий статус выполнения задач: airflow_раб_дз1-4.png
2. Проверка загрузки в PostgreSQL: ДЗ4postgres_загрузка_данных.png
3. Этапы фильтрации и очистки: ДЗ2_фильтрация данных.png

## Инструкция по запуску
1. Склонируйте репозиторий.
2. Перейдите в директорию проекта: cd airflow_training
3. Запустите инфраструктуру: docker-compose up -d
4. Доступ к сервисам:
    * Airflow: http://localhost:8080 (логин: admin, пароль: admin)
    * Jupyter Lab: http://localhost:8888 (рабочая папка /work)

Все итоговые CSV-файлы и программный код DAG доступны для проверки в директории airflow_training/airflow/dags/.



*описание составленно с приминенем техонологии нейросетей
