from bs4 import BeautifulSoup
import requests, json
from requests_html import HTML, HTMLSession
from selenium import webdriver
from time import time

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }

url ='https://coinmarketcap.com/nft/upcoming/?page='
html_txt = ''
h=0
for i in range(1,2):

    response = requests.get(url + str(i), headers=headers)
    html_txt += response.text

soup = BeautifulSoup(html_txt, 'html.parser')
cont = soup.find_all('tr')

for i in cont:
    try:
        name=i.find('div', {'class':'sc-15yqupo-0 cqAZPF'}).contents[0].find('span').text
        network = i.find('div', {'class': 'sc-15yqupo-0 cqAZPF'}).contents[0].find('span').next_sibling.text
        description = i.find('div', {'class': 'sc-15yqupo-0 cqAZPF'}).contents[1].text
        social_1 = i.find('div', {'class': "sc-15yqupo-1 gEtvIk"}).contents[0].a['href']
        social_2 = i.find('div', {'class': "sc-15yqupo-1 gEtvIk"}).contents[1].a['href']
        social_3 = i.find('div', {'class': "sc-15yqupo-1 gEtvIk"}).contents[2].a['href']
        data=i.find('div', {'class': "sc-15yqupo-2 dhMNvT"}).contents[1].text
        price=i.find('div', {'class': "sc-1ay2tc4-0 dRIGnz"}).contents[-1].text
        image= i.find('div', {'class': "sc-1ay2tc4-1 lhOERa"})
#
#         #if "__INITIAL_STATE__" in i.text:
#         print(image)
#         #print(image_1)
#     except:
#         pass




# page = requests.get('')
# soup = BeautifulSoup(page.content, 'html.parser')https://coinmarketcap.com/nft/upcoming
#
# script = None
# for s in soup.find_all("img"):
#     if "__INITIAL_STATE__" in s.text:
#         script = s.get_text(strip=True)
#         print('hi')
#         break

#data = json.loads(script[script.index('{'):script.index('function')-2])

# with open("data.json", "w") as f:
#     json.dump(data, f)

# print(s)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome('C:/Users/Owner/PycharmProjects/final_project/aphorism/chromedriver/chromedriver.exe')

whole_url = 'https://coinmarketcap.com/nft/upcoming'
driver.get(whole_url)
wait = WebDriverWait(driver, 50)
wait.until(EC.visibility_of_element_located((By.XPATH, "//img")))
with open('parse.html', 'w') as f:
    f.write(driver.page_source)

images = driver.find_elements(By.TAG_NAME, 'img')
#print(images)
pfp = ""
for image in images:
    pfp = (image.get_attribute('src'))
    print(pfp)
driver.close()
#<img src="https://i.imgur.com/1zoSrhm.png" class="sc-1ehai65-0 ctNIkQ  lazy-load loaded ">