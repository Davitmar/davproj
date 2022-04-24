from flask import Flask, render_template
import requests

app=Flask(__name__)

@app.route('/wheather/<lon>/<lat>')
def wheather(lon,lat):
    l=0
    url = f'https://www.7timer.info/bin/astro.php?lon={lon}&lat={lat}&ac=0&unit=metric&output=json&tzshift=0'
    resp=requests.get(url)#, headers={'Accept':'application/json'})
    js= resp.json()
    for i in js["dataseries"]:
        l+=i['temp2m']
    return f'lon:{lon} and lat:{lat} average temperature is < {round(l/len(js["dataseries"]), 1)} > gr. of celsius'

if __name__=='__main__':
    app.run(debug=True)