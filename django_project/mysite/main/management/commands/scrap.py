from django.core.management.base import BaseCommand
from main.models import University, Country
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        url = 'https://cwur.org/2021-22.php'
        response = requests.get(url, headers=headers)
        html_txt = response.text
        soup = BeautifulSoup(html_txt, 'html.parser')
        cont = soup.find(id='cwurTable').find_all('tr')



        for j in cont[1:]:
            name = j.contents[2].text
            country, _ = Country.objects.get_or_create(name=name)


            univ = University(rank=j.contents[0].text, name=j.contents[1].text, country=country,
                                  score=j.contents[-1].text)
            univ.save()