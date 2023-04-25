

import requests


base_url = "http://127.0.0.1:5555"

# Log in and retrieve the JWT token
login_data = {
    "username": "samcoelho",
    "password": "sam",
}
response = requests.post(f"http://127.0.0.1:5555/login", json=login_data)

if response.status_code == 200:
    jwt_token = response.json()["access_token"]

    # Access a protected route using the JWT token
    headers = {
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MjQxMTQwMiwianRpIjoiYmRhYmJlMzYtZjczYi00ZDMwLTliZmMtN2YyYTBiY2U0NzUzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NSwibmJmIjoxNjgyNDExNDAyLCJleHAiOjE2ODI0MTIzMDJ9.6YGfNf2gIM7HDTMtkSL7THIi2Jn3E9F89UlL1OUlDPQ",
        "Content-Type": "application/json",
    }
    protected_route = f"http://127.0.0.1:5555/user/1/walks" 
    response = requests.get(protected_route, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: {response.status_code} - {response.json().get('msg', response.json())}")
else:
    print(f"Error: {response.status_code} - {response.json().get('msg', response.json())}")