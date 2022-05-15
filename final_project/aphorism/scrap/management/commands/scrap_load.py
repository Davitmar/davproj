from django.core.management.base import BaseCommand
from scrap.models import Quotas, Authors, Tags
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        url = 'https://quotes.toscrape.com/page/'
        html_txt = ''
        for i in range(1, 11):
            response = requests.get(url + str(i), headers=headers)
            html_txt += response.text
        soup = BeautifulSoup(html_txt, 'html.parser')
        cont = soup.find_all('div', {'class': 'quote'})
        tag_list = []
        for j in cont:
            author = j.find('small', {'class': 'author'}).contents[0].text
            a, _ = Authors.objects.get_or_create(author=author)

            quota = j.find('span', {'class': 'text'}).contents[0].text
            q = Quotas(quota=quota, author=a)
            q.save()

            l = j.find_all('a', {'class': 'tag'})
            for k in l:
                tag = k.text
                t, _ = Tags.objects.get_or_create(tag=tag)

                q.tag.add(t)
        #
        # Authors.objects.all().delete()
        # Tags.objects.all().delete()
        #
        # Quotas.objects.all().delete()

        #print(Quotas.objects.values('tag'))
