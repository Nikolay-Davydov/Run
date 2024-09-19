import requests
import webbrowser

CLIENT_ID = '132792'
CLIENT_SECRET = '01f5b78c7d1c6304d4997ae2852f7f8f901c2456'
REDIRECT_URI = 'http://localhost:8080/callback'

# Шаг 1: Направляем пользователя на URL авторизации
auth_url = (
    f"https://www.strava.com/oauth/authorize"
    f"?client_id={CLIENT_ID}"
    f"&response_type=code"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=read,activity:read"
    )

print("Откройте этот URL для авторизации:", auth_url)
webbrowser.open(auth_url)

# Шаг 2: Получение токена доступа (замените на ваш код авторизации)
# http://localhost:8080/callback?state=&code=887694973a95bc999107e975b2b17032ca35b666&scope=read,activity:read
AUTHORIZATION_CODE = '887694973a95bc999107e975b2b17032ca35b666'

token_url = 'https://www.strava.com/oauth/token'
token_data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': AUTHORIZATION_CODE,
    'grant_type': 'authorization_code'
}

response = requests.post(token_url, data=token_data)
token_response = response.json()

print("Token Response:", token_response)
access_token = token_response['access_token']
refresh_token = token_response['refresh_token']

# Шаг 3: Обновление токена доступа (если необходимо)
refresh_data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
}
response = requests.post(token_url, data=refresh_data)
new_token_response = response.json()

print("New Token Response:", new_token_response)
new_access_token = new_token_response['access_token']
new_refresh_token = new_token_response['refresh_token']

# Шаг 4: Получение данных активности
activities_url = 'https://www.strava.com/api/v3/athlete/activities'
headers = {
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(activities_url, headers=headers)
activities = response.json()

print("Activities:", activities)