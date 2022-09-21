from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule
import time
import urllib3

app = Flask(__name__)

url_list = [
'https://www.google.com/search?client=opera-gx&q=CACR11&sourceid=opera&ie=UTF-8&oe=UTF-8',
'https://www.google.com/search?client=opera-gx&q=OUJP11&sourceid=opera&ie=UTF-8&oe=UTF-8',
'https://www.google.com/search?client=opera-gx&q=PLCR11&sourceid=opera&ie=UTF-8&oe=UTF-8',
'https://www.google.com/search?client=opera-gx&q=RBHG11&sourceid=opera&ie=UTF-8&oe=UTF-8',
'https://www.google.com/search?client=opera-gx&q=IRBR3&sourceid=opera&ie=UTF-8&oe=UTF-8',
'https://www.google.com/search?client=opera-gx&q=KLBN4F&sourceid=opera&ie=UTF-8&oe=UTF-8'
]

price_list = []
stock_list = ['CACR11', 'OUJP11', 'PLCR11','RBHG11','IRBR3', 'KLBN4F']
date_list = []

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@app.route('/', methods=("POST", "GET"))
def job():
    for elemento in url_list:
        stock(elemento)
        if elemento == 'https://www.google.com/search?client=opera-gx&q=KLBN4F&sourceid=opera&ie=UTF-8&oe=UTF-8':
            information = pd.DataFrame({'Acao':stock_list, 'Preço':price_list, 'Data':date_list})
            price_info = pd.DataFrame({'Preço':price_list})
            price_final = price_info
            info_final = information
            del information
            del price_info
            date_list.clear()
            price_list.clear()
            return render_template('index.html',  tables=[info_final.to_html(classes='data', header="true"), price_final.to_html(classes='data', header="true")])       

def stock(elemento):    
    html = requests.get(elemento, timeout=3, verify=False)
    soup = BeautifulSoup(html.text, 'html.parser')
    
    date = soup.find(class_="nXE3Ob")
    date_list.append(date.text[0:20])
    
    price = soup.find(class_="BNeawe iBp4i AP7Wnd")
    price_list.append(price.text)
    html.close()


if __name__ == '__main__':
    app.run()


schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(2)

