import requests
import pandas as pd
import json

# Get jwt token for authorization
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
    
# Update api with value --> (courses , categories , ...)
def update_api_key_courses(value):
    API_KEY = f'https://api.movazee.ir/v1/dashboard/manage/{value}/'
    return API_KEY

def update_api_key_chapter(parent , id_value , child):
    API_KEY = f'https://api.movazee.ir/v1/dashboard/manage/{parent}/{id_value}/{child}'
    return API_KEY 


# Get api data for check values and raplace to csv data
def get_api_data(value):
    headers = {
    "Authorization": f"Bearer {login_to_api()}",
    "Content-Type": "application/json",
    }
    res = requests.get(url = update_api_key_courses(value) , headers = headers)
    if res.status_code == 200:
        return res.json()
    else:
        return 'error bad request'

# Change values --> (categories , tags , users) to therer id for {Courses data}
def check_json_value(value , json_data , topic):
    data_id = {}
    if topic == 'Course':
        for item in json_data['data']:
            data_id[item['title']] = item['id']
            for child in item['children']:
                data_id[child['title']] = child['id']
        for id in data_id:
            if id == value:
                return data_id[id]
    elif topic == 'Username':
        for item in json_data['data']:
            data_id[item['username']] = item['id']
        for id in data_id:
            if id == value:
                return data_id[id]
    elif topic == 'Tag':
        for item in json_data['data']:
            data_id[item['title']] = item['id']
        for id in data_id:
            if id == value:
                return data_id[id]
def change_title_to_id(dict_data):
    for category in range(len(dict_data['categories'])):
        id_value = check_json_value(dict_data['categories'][category] , get_api_data('categories') , 'Course')
        if id_value:
            dict_data['categories'][category] = id_value

    for user in range(len(dict_data['instructors'])):
        id_value = check_json_value(dict_data['instructors'][user] , get_api_data('users') , 'Username')
        if id_value:
            dict_data['instructors'][user] = id_value

    for tag in range(len(dict_data['tags'])):
        id_value = check_json_value(dict_data['tags'][tag] , get_api_data('tags') , 'Tag')
        if id_value:
            dict_data['tags'][tag] = id_value
    return dict_data


# Post data to api
def post_data_course(dict_data , value):
    headers = {
    "Authorization": f"Bearer {login_to_api()}",
    "Content-Type": "application/json",
    }
    res = requests.post(url = update_api_key_courses(value) , json = dict_data , headers = headers)
    if res.status_code == 201 or res.status_code == 200:
        return res.json()
    else:
        return res.json()

def post_data_chapter(dict_data , parent , id_value , child):
    headers = {
    "Authorization": f"Bearer {login_to_api()}",
    "Content-Type": "application/json",
    }
    res = requests.post(url = update_api_key_chapter(parent , id_value , child) , json = dict_data , headers = headers)
    if res.status_code == 201 or res.status_code == 200:
        return res.json()
    else:
        return res.json()

# Get csv file and extract data
def get_csv_file(csv_file):
    csv = pd.read_csv(csv_file)
    dict_data = {}
    course_data = {}
    chapter_data = {}
    lesson_data = {}
    step_data = {}
    fields_to_keep_as_list = ['Course categories', 'Course instructors', 'Course tags']
    for i in csv.columns:
        filter_value = csv[i].dropna().to_list()
        if i.startswith('Course'):
            if i in fields_to_keep_as_list:
                dict_data[i] = filter_value
            else:
                for j in filter_value:
                    dict_data[i] = j
        else:
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

    course_json = post_data_course(change_title_to_id(course_data) , 'courses')
    print(course_json)
    course_id = course_json['data']['id']
    # # course_id = 78

    chapter_titles = {}
    lesson_titles = {}
    data = chapter_data
    num_items = len(list(data.values())[0]) 
    for idx in range(num_items):
        single_item_data = {}
        for key in data:
            if idx < len(data[key]) and data[key][idx]:
                single_item_data[key] = data[key][idx]
        if single_item_data:
            single_item_data['course'] = course_id
            chapter_json = post_data_chapter(single_item_data , 'courses' , str(course_id) , 'chapters')
            title = chapter_json['data']['title']
            id_value = chapter_json['data']['id']
            chapter_titles[title] = id_value
            print(chapter_json)

    data = lesson_data
    num_items = len(list(data.values())[0]) 
    for idx in range(num_items):
        single_item_data = {}
        for key in data:
            if idx < len(data[key]) and data[key][idx]:
                single_item_data[key] = data[key][idx]
        if single_item_data:
            if single_item_data['chapter'] in chapter_titles:
                value = chapter_titles[single_item_data['chapter']]
                single_item_data['chapter'] = value
            lesson_json = post_data_chapter(single_item_data , 'chapters' , str(single_item_data['chapter']) , 'lessons')
            title = lesson_json['data']['title']
            id_value = lesson_json['data']['id']
            lesson_titles[title] = id_value
            print(lesson_json)


    data = step_data
    num_items = len(list(data.values())[0])
    for idx in range(num_items):
        single_item_data = {}
        for key in data:
            if idx < len(data[key]) and data[key][idx]:
                single_item_data[key] = data[key][idx]
        if single_item_data:
            if single_item_data['lesson'] in lesson_titles:
                value = lesson_titles[single_item_data['lesson']]
                single_item_data['lesson'] = value
            step_json = post_data_chapter(single_item_data , 'lessons' , str(single_item_data['lesson']) , 'steps')
            print(step_json)
            

            
csv_file = 'ASA.csv'
title = 'ریکت'
get_csv_file(csv_file)
# print(get_csv_file(csv_file))
# print(get_api_data('users'))
# print(check_json_value(title , get_api_data('categories')))
# print(check_json_value_username(username  , get_api_data('users')))
# print(change_title_to_id(get_csv_file(csv_file , 'mmd')))
# change_title_to_id(get_csv_file(csv_file))

