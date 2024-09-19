# step4_get_activities.py
import requests

from api_code import ACTIVITIES_URL


def get_access_token_from_file():
    with open('tokens.txt', 'r') as f:
        lines = f.readlines()
        access_token = [line.split('=')[1].strip() for line in lines if line.startswith('access_token=')][0]
    return access_token


# ACTIVITIES_URL = 'https://www.strava.com/api/v3/athlete/activities'


def get_activities(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(ACTIVITIES_URL, headers=headers)
    return response.json()


if __name__ == "__main__":
    access_token = get_access_token_from_file()
    activities = get_activities(access_token)
    print("Activities:", activities)
