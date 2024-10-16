import requests
import pandas as pd
import json

# API_KEY = f'https://api.movazee.ir/v1/dashboard/manage/corses/'

def login_to_api():
    
    url = "http://api.movazee.ir/v1/auth/login/"
    body = {
        "username": "Hamed_Fakoori",
        "password": "Hamed_Movazee@Admin"
    }

    response = requests.post(url, json = body)

    if response.status_code == 200:
        data = response.json()
        
        return data['data'].get('access')
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def update_api_key(value):
    API_KEY = f'https://api.movazee.ir/v1/dashboard/manage/{value}/'
    return API_KEY

def get_api_data(value):
    headers = {
    "Authorization": f"Bearer {login_to_api()}",
    "Content-Type": "application/json",
    }
    res = requests.get(url = update_api_key(value) , headers = headers)
    if res.status_code == 200:
        return res.json()
    else:
        return 'error bad request'

def check_json_value(title , json_data):
    data_id = {}
    for item in json_data['data']:
        data_id[item['title']] = item['id']
        for child in item['children']:
            data_id[child['title']] = child['id']
    for id in data_id:
        if id == title:
            return data_id[id]

def get_csv_file(csv_file):
    csv = pd.read_csv(csv_file)
    dict_data = {}
    for i in csv.columns:
        filter_value = csv[i].dropna().to_list()
        if filter_value:
            dict_data[i] = filter_value
    return dict_data
    
def change_title_to_id(dict_data):
    for i in range(len(dict_data['Title'])):
        id_value = check_json_value(dict_data['Title'][i] , get_api_data('categories'))
        if id_value:
            dict_data['Title'][i] = id_value
    return dict_data



csv_file = 'ASA.csv'
title = 'پایتون'
# print(get_csv_file(csv_file))
# print(get_api_data('categories'))
# print(check_json_value(title , get_api_data('categories')))
print(change_title_to_id(get_csv_file(csv_file)))
# change_title_to_id(get_csv_file(csv_file))

