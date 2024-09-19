# step2_get_token.py
import requests
# from authorize import CLIENT_ID, CLIENT_SECRET  # Импортируем переменные из предыдущего файла
from api_code import TOKEN_URL, CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_CODE

# TOKEN_URL = 'https://www.strava.com/oauth/token'


def get_access_token(client_id, client_secret, authorization_code):
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_URL, data=token_data)
    return response.json()


if __name__ == "__main__":
    # AUTHORIZATION_CODE = '7a298862c16acd236cf7ee9603af3b5cb2f37ec4'  # Замените на код авторизации
    token_response = get_access_token(CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_CODE)
    print("Token Response:", token_response)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    # Сохраняем токены в файл для последующего использования
    with open('tokens.txt', 'w') as f:
        f.write(f'access_token={access_token}\n')
        f.write(f'refresh_token={refresh_token}\n')
