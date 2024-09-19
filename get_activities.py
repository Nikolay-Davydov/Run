import requests
import logging
import json
import os
from api_code import ACTIVITIES_URL

logging.basicConfig(level=logging.INFO)

def get_access_token_from_file(file_path='tokens.txt'):
    """Получает токен доступа из файла. Генерирует исключения в случае неудачи."""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            access_token = [line.split('=')[1].strip() for line in lines if line.startswith('access_token=')]
            if not access_token:
                raise ValueError("Токен доступа не найден в файле.")
            return access_token[0]
    except FileNotFoundError:
        logging.error("Файл с токеном не найден.")
        raise
    except Exception as e:
        logging.error(f"Ошибка при получении токена доступа: {e}")
        raise

def load_existing_data(file_path='activities.json'):
    """Загружает существующие данные из файла, если файл существует."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                logging.info(f"Существующие данные загружены из {file_path}")
                return data
        except json.JSONDecodeError:
            logging.error(f"Ошибка при чтении данных из {file_path}. Файл повреждён или не является корректным JSON.")
            return []
        except Exception as e:
            logging.error(f"Ошибка при чтении файла {file_path}: {e}")
            raise
    else:
        logging.info(f"Файл {file_path} не найден. Будет создан новый файл.")
        return []

def save_to_file(data, file_path='activities.json'):
    """Сохраняет данные в формате JSON в указанный файл."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Данные успешно сохранены в {file_path}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в файл: {e}")
        raise

def get_activities(access_token, output_file='activities.json'):
    """Отправляет API-запрос и добавляет новые данные в файл. Включает обработку ошибок."""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    try:
        response = requests.get(ACTIVITIES_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Генерирует исключение для ответов с кодом 4xx/5xx
        try:
            new_data = response.json()

            # Загружаем существующие данные, если файл существует
            existing_data = load_existing_data(output_file)

            # Проверим, есть ли новые данные
            if new_data not in existing_data:
                existing_data.append(new_data)
                save_to_file(existing_data, output_file)  # Сохраняем обновлённые данные
            else:
                logging.info("Полученные данные уже существуют в файле.")

            return new_data
        except ValueError:
            logging.error("Ответ от API не в формате JSON.")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при выполнении API-запроса: {e}")
        return None

if __name__ == "__main__":
    try:
        access_token = get_access_token_from_file()
        activities = get_activities(access_token)
        if activities:
            logging.info(f"Данные получены и обработаны.")
        else:
            logging.error("Не удалось получить данные.")
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

