from requests import Session
import re


def download_tik(url: str):
    host = 'https://ssstik.io/abc?url=dl'
    data = {'id': url, 'locale': 'en', 'tt': 'NHBveDE5'}
    s = Session()
    s.cookies.clear()
    s.max_redirects = 30
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    })
    r = s.post(host, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if r.status_code == 200:
        pattern = r'<a href="([^"]+)"'
        match = re.search(pattern, r.text)
        return match.group(1)
    return None
