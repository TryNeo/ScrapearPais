#!/bin/env python
import logging
import threading
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level = logging.INFO,
    format='%(message)s'
)

URL = 'https://es.wikipedia.org/wiki/Wikiproyecto:Ciudades/Capitales_de_pa%C3%ADses'


def error():
    logging.error('Ops Lo siento error de Conexion')


def get_pais_capital(content):
    pais_capital = []
    f = open('countries.csv','w')
    f.write("pais,")
    f.write("capital\n")
    soup = BeautifulSoup(content,'html.parser')
    for pc in soup.find_all('div',class_='mw-parser-output'):
        for row in pc.table.select("tbody > tr")[1::]:
            tds = row.select('td')
            f.write(tds[1].text+",")
            f.write(tds[0].text+"\n")
        


def get_reponse(url,success_callback,error_callback):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            success_callback(content)
    except requests.exceptions.ConnectionError:
        error_callback()

if __name__ == "__main__":
    thread = threading.Thread(
        target=get_reponse,
        kwargs={
            'url':URL,
            'success_callback':get_pais_capital,
            'error_callback':error,
        }
    )
    
    thread.start()