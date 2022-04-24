# import requests
#
# def wh(lon,lat):
#     l=[]
#     url = f'https://www.7timer.info/bin/astro.php?lon={lon}&lat={lat}&ac=0&unit=metric&output=json&tzshift=0'
#     resp=requests.get(url)
#     for i in resp.json()["dataseries"]:
#         l.append(i['temp2m'])
#     return round(sum(l)/len(l),1)
#
#
#
# print(wh(40.9,25.4))
from hashlib import sha256
def coding(a):
    c=sha256(a.encode('utf-8')).hexdigest())
    return c