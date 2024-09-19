# step3_refresh_token.py
import requests
from api_code import TOKEN_URL, CLIENT_ID, CLIENT_SECRET

# CLIENT_ID = 'your_client_id'
# CLIENT_SECRET = 'your_client_secret'
# TOKEN_URL = 'https://www.strava.com/oauth/token'


def refresh_access_token(client_id, client_secret, refresh_token):
    refresh_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(TOKEN_URL, data=refresh_data)
    return response.json()


if __name__ == "__main__":
    # Читаем сохраненные токены
    with open('tokens.txt', 'r') as f:
        lines = f.readlines()
        refresh_token = [line.split('=')[1].strip() for line in lines if line.startswith('refresh_token=')][0]

    new_token_response = refresh_access_token(CLIENT_ID, CLIENT_SECRET, refresh_token)
    print("New Token Response:", new_token_response)

    new_access_token = new_token_response['access_token']
    new_refresh_token = new_token_response['refresh_token']

    # Сохраняем обновленные токены
    with open('tokens.txt', 'w') as f:
        f.write(f'access_token={new_access_token}\n')
        f.write(f'refresh_token={new_refresh_token}\n')
