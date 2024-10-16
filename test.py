import requests

def login_to_api():
    
    url = "http://api.movazee.ir/v1/auth/login/"
    body = {
        "username": "Hamed_Fakoori",
        "password": "Hamed_Movazee@Admin"
    }

    response = requests.post(url, json=body)

    if response.status_code == 200:
        data = response.json()
        
        return data['data'].get('access')
    else:
        return f"Error: {response.status_code}, {response.text}"


access_token = login_to_api()
print(access_token)
