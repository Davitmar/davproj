import requests
from bs4 import BeautifulSoup


def get_universities():
    url = 'https://cwur.org/2021-22.php'
    response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'})

    response_html = response.text

    soup = BeautifulSoup(response_html, 'html.parser')

    all_data = []
    for trow in soup.select('table#cwurTable tbody tr'):
        trow = trow.contents
        all_data.append({
            'rank': trow[0].text,
            'name': trow[1].text,
            'country': trow[2].text,
            'score': trow[-1].text
        })
    return all_data