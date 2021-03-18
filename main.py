#!/usr/bin/env python3
from elasticsearch import Elasticsearch
import requests
import json
from datetime import date, datetime
from measurement import Measurement


#    'https://data.cityofchicago.org/resource/crimes.json?$limit=1000000000'


def get_data(url):
    resp = requests.get(url)
    temp = resp.json()
    return temp


def crime_data_points(resp: dict):
    obj_list = []
    print(resp)
    for crime_data in resp:
        crime = Measurement(**crime_data)
        obj_list.append(crime.serialize())
    print(obj_list)
    return obj_list


# def create_df(response: dict):
#     headers = list(response[0].keys())
#     values = [list(i.values()) for i in response]
#     for sublist in response:
#         print(sublist)
#     # df = pd.DataFrame(columns=headers, data=values)
#     print(headers)
#     # print(values)
#     # return df
#
#
# def transformation_df(df):
#     df['start_date'] = df['date'].apply(pd.to_datetime, format='%Y-%m-%d')
#     df['hours'] = df['date'].apply(pd.to_datetime, format='%H:%M:%S')
#     print(df.to_string())
#     return df


def send_data(data_list: list):
    es = Elasticsearch(['35.246.157.251:9200'])
    for body in data_list:
        short_time_id = body['crime_date'][:-7]
        short_update_id = body['updated_on'][:-7]
        date_now = str(datetime.now())[:-7]
        resp = es.index(
            index='crime3',
            doc_type='_doc',
            body=body,
            id=body['case_number']+'_'+body['crime_id']+'_'+short_time_id+'_'+short_update_id,
            request_timeout=30)
        print(body)
        print(resp,'\n')

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
