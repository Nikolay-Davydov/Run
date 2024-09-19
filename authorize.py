# step1_authorize.py
import webbrowser

from api_code import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI  # Импортируем переменные из предыдущего файла


def get_auth_url(client_id, redirect_uri):
    return (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope=read,activity:read"
    )


def open_auth_url(auth_url):
    print("Откройте этот URL для авторизации:", auth_url)
    webbrowser.open(auth_url)


if __name__ == "__main__":
    auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)
    open_auth_url(auth_url)
