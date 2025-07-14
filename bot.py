import requests
import time

TOKEN = '8183994614:AAEiVXbVroi0SmMSrQbiK8lSHNAykz-pTZg'
URL = f'https://api.telegram.org/bot{TOKEN}/'

def get_updates(offset=None):
    url = URL + 'getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = URL + 'sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    requests.post(url, params=params)

def search_profiles(username):
    platforms = {
        'Instagram': f'https://www.instagram.com/{username}/',
        'GitHub': f'https://github.com/{username}',
        'Twitter (X)': f'https://twitter.com/{username}',
        'TikTok': f'https://www.tiktok.com/@{username}',
        'Reddit': f'https://www.reddit.com/user/{username}',
        'VK': f'https://vk.com/{username}',
        'Facebook': f'https://www.facebook.com/{username}',
        'YouTube': f'https://www.youtube.com/@{username}',
        'Pinterest': f'https://www.pinterest.com/{username}/',
        'LinkedIn': f'https://www.linkedin.com/in/{username}/',
        'Steam': f'https://steamcommunity.com/id/{username}',
        'Medium': f'https://medium.com/@{username}',
        'Spotify': f'https://open.spotify.com/user/{username}',
        'Telegram': f'https://t.me/{username}',
        'Snapchat': f'https://www.snapchat.com/add/{username}'
    }

    result = f'🔍 Профили для ника: {username}\n\n'

    for site, url in platforms.items():
        try:
            r = requests.get(url)
            if r.status_code == 200:
                result += f'✅ {site}: {url}\n'
            else:
                result += f'❌ {site}: не найдено\n'
        except:
            result += f'⚠️ {site}: ошибка при проверке\n'

    return result

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if 'result' in updates:
            for update in updates['result']:
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    message_text = update['message'].get('text', '')

                    if message_text == '/start':
                        send_message(chat_id, '👋 Привет! Отправь мне ник, и я проверю соцсети.')
                    else:
                        response = search_profiles(message_text)
                        send_message(chat_id, response)

                    last_update_id = update['update_id'] + 1
        time.sleep(0.5)

if __name__ == '__main__':
    main()
