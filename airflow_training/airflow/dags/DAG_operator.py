from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd
import requests
import re
import xml.etree.ElementTree as ET
import os



SAVE_PATH = '/opt/airflow/dags/'
RAW_PETS_DATA = "https://raw.githubusercontent.com/LearnWebCode/json-example/refs/heads/master/pets-data.json"
RAW_NUTRION = "https://gist.githubusercontent.com/pamelafox/3000322/raw/6cc03bccf04ede0e16564926956675794efe5191/nutrition.xml"



def clean_html(raw_html):
    clean_r = re.compile('<.*?>')
    return re.sub(clean_r, '', raw_html)

def nutrion_get():
    r_nutr = requests.get(RAW_NUTRION)
    root = ET.fromstring(r_nutr.text) 
    food_list = []
    
    for food in root.findall('food'): 
        item = {
            "product_name": food.find('name').text.strip(),
            "mfr": food.find('mfr').text.strip(),
            "total_calories": food.find('calories').get('total'),
        }

        vitamins = food.find('vitamins')
        if vitamins is not None:
            for vit in vitamins:
                item[f"vit_{vit.tag}"] = vit.text

        minerals = food.find('minerals')
        if minerals is not None:
            for min_el in minerals:
                item[f"min_{min_el.tag}"] = min_el.text
    
        food_list.append(item)

    df = pd.DataFrame(food_list)

    engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')
    df.to_sql('nutrition', engine, if_exists='replace', index=False)
    print("Данные о питании успешно загружены в Postgres")



def pets_get():
    r_pets = requests.get(RAW_PETS_DATA)
    if r_pets.status_code == 200:
        data = r_pets.json()
        flat_pets = []
        
        for pet in data['pets']:
            name = pet.get('name')
            species = pet.get('species')
            year = pet.get('birthYear')
    
            foods_list = [clean_html(food) for food in pet.get('favFoods', [])]
            foods_str = ", ".join(foods_list)

            flat_pet = {
                "name": name,
                "species": species,
                "birth_year": year,
                "favorite_foods": foods_str
            }
            flat_pets.append(flat_pet)
        df = pd.DataFrame(flat_pets)

        engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres:5432/airflow')
        df.to_sql('pets', engine, if_exists='replace', index=False)
        print("Данные питомцев успешно загружены в Postgres")



with DAG(
    dag_id='data_sources_transform',
    start_date=datetime(2026, 1, 24),
    schedule_interval=None,
    catchup=False
) as dag:

    task_json = PythonOperator(
        task_id='transform_pets_json',
        python_callable=pets_get
    )

    task_xml = PythonOperator(
        task_id='transform_nutrition_xml',
        python_callable=nutrion_get
    )

    task_json >> task_xml
 
