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
        
def check_json_value_username(username , json_data):
    data_id = {}
    for item in json_data['data']:
        data_id[item['username']] = item['id']
    for id in data_id:
        if id == username:
            return data_id[id]

def get_csv_file(csv_file , value):
    csv = pd.read_csv(csv_file)
    dict_data = {}
    course_data = {}
    chapter_data = {}
    lesson_data = {}
    step_data = {}
    for i in csv.columns:
        filter_value = csv[i].dropna().to_list()
        if filter_value:
            dict_data[i] = filter_value

    for j in dict_data:
        if j.startswith('Course '):
            new_key = j.replace('Course ', '')
            course_data[new_key] = dict_data[j]
        elif j.startswith('Chapter '):
            new_key = j.replace('Chapter ', '')
            chapter_data[new_key] = dict_data[j]
        elif j.startswith('Lesson '):
            new_key = j.replace('Lesson ', '')
            lesson_data[new_key] = dict_data[j]
        elif j.startswith('Step '):
            new_key = j.replace('Step ', '')
            step_data[new_key] = dict_data[j]

    if value == 'Course':
        return course_data
    elif value == 'Chapter':
        return chapter_data
    elif value == 'Lesson':
        return lesson_data
    elif value == 'Step':
            return step_data


def change_title_to_id(dict_data):
    for i in range(len(dict_data['Title'])):
        id_value = check_json_value(dict_data['Title'][i] , get_api_data('categories'))
        if id_value:
            dict_data['Title'][i] = id_value

    for j in range(len(dict_data['Instructors'])):
        id_value = check_json_value_username(dict_data['Instructors'][j] , get_api_data('users'))
        if id_value:
            dict_data['Instructors'][j] = id_value
    return dict_data




csv_file = 'ASA.csv'
value = 'Course'
title = 'پایتون'
username = 'AliAsgharFathikhah'
# print(get_csv_file(csv_file , value))
# print(get_api_data('users'))
# print(check_json_value(title , get_api_data('categories')))
# print(check_json_value_username(username  , get_api_data('users')))
# print(change_title_to_id(get_csv_file(csv_file , value)))
# change_title_to_id(get_csv_file(csv_file))

