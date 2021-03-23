#!/usr/bin/env python3
import os
import requests
import json
import dotenv

from datetime import date, datetime
from elasticsearch import Elasticsearch

from measurement import Measurement

dotenv.load_dotenv()
es = Elasticsearch([os.environ['ELK_ADDRES']])


def get_data(url):
    resp = requests.get(url)
    temp = resp.json()
    return temp


def crime_data_points(resp: dict):
    obj_list = []
    print(resp)
    for crime_data in resp:
        crime = Measurement(**crime_data)
        print(crime_data)
        obj_list.append(crime.serialize())
    print(obj_list)
    return obj_list

    ''' Funkcja
    :param data_list: list - parametr przyjmuje liste z serializowanych obiektów klasy measurement'''

def send_data(data_list: list):
    for body in data_list:
        resp = es.index(
            index='crime3',
            doc_type='_doc',
            body=body,
            id=f"{body['case_number']}_{body['crime_id']}_{body['create_id']}",
            request_timeout=30)
        print("Sending to Elasticsearch: ", body)
        print("Elasticsearch response: ", resp, '\n')


def save_data(data_list: list):
    filename = 'crime_'+ str(date.today())+'.json'
    with open(filename, 'a') as f_obj:
        json.dump(data_list, f_obj)

if __name__ == '__main__':
    for i in range(0, 10000000000000, 1000):
        print(i)
        data = get_data(f'https://data.cityofchicago.org/resource/crimes.json?$limit=1000&$offset={i}')
        data_list = crime_data_points(data)
        # transformation/dataframe function
        send_data(data_list)
        save_data(data_list)
        if len(data) == 0:
            break
