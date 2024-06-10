import requests
import json
from collections import deque


def get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    return response.text


def get_reddit_thread_body(url):
    url = url + ".json"
    data = get(url)
    if not data:
        return ""
    data_json = json.loads(data)
    queue = deque(data_json)
    output = []
    while queue:
        obj = queue.popleft()
        if isinstance(obj, dict):
            for key in obj:
                if key == 'body':
                    output.append(obj[key])
                else:
                    if obj[key] and isinstance(obj[key], list):
                        for item in obj[key]:
                            queue.append(item)
                    elif obj[key] and isinstance(obj[key], dict):
                        queue.append(obj[key])
        elif obj and isinstance(obj, list):
            for item in obj:
                queue.append(item)
    return output


if __name__ == '__main__':
    print(len(get_reddit_thread_body(
        "https://www.reddit.com/r/Entrepreneur/comments/1d65jhl/most_influential_books_you_ever_read")))
