from bs4 import BeautifulSoup
from urllib import request

def get_html(url):
    response = request.urlopen(url)
    return response.read()

def parser():
    html1 = get_html('http://flights.charmeck.org/mnt/FlightsMain.asp?sk=uNZg3kNlRnqsuOL')
    soup1 = BeautifulSoup(html1)
    table1 = soup1.find('table')
    print(table1)
    return

parser()
