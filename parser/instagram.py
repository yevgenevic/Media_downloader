import httpx


def download_insta(url: str):
    host = f"http://95.163.241.85:8000/reel/url?url={url}"
    params = {'url': url}
    response = httpx.get(host, params=params)
    return response.json()


