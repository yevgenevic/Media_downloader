import httpx
import json


def download_story(username: str):
    url = f"http://95.163.241.85:8000/story/username?username={username}"
    params = {'username': username}
    try:
        response = httpx.get(url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            return response.status_code

    except Exception as e:
        return f"Request failed: {e}"


def profile(username: str):
    response = download_story(username)
    try:
        data = json.loads(response)
    except (json.JSONDecodeError, TypeError) :
        return f"Private profile"

    if all(key in data for key in ['profile_pic_url', 'followers', 'following', 'full_name']):
        return (
            data['profile_pic_url'],
            data['followers'],
            data['following'],
            data['full_name']
        )
    else:
        return f"Error: Missing expected keys in JSON response"


def stories_list(username: str):
    response = download_story(username)
    try:
        data = json.loads(response)
        stories = data.get('stories', [])
        return [story.get('source', '') for story in stories]
    except json.JSONDecodeError as e:
        return [f"Error decoding JSON: {e}"]
    except Exception as e:
        return [f"Error: {e}"]
