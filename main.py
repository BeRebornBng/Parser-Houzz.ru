import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import configparser
from concurrent.futures import ThreadPoolExecutor

url = "https://www.houzz.ru/professionals/"
spec = ''
index = ''

myArray = []
def Parser(value):
    global myArray
    global spec
    global index
    config = configparser.ConfigParser()
    config.read('MyData.ini')
    spec = config['Link']['spec']
    index = '/c/' + config['Link']['index']

    response = requests.get(value)
    soup = BeautifulSoup(response.text, 'html.parser')

    tel = json.loads(soup.find('div', 'hz-page-content-wrapper').find('script').text)

    myDict = {'Наименование': '',
              'Сайт HOUZ': '',
              'Сайт': '',
              'Номер телефона': '',
              'Адрес': '',
              'О нас': '',
              'Предоставляемые услуги': '',
              'География работ': '',
              'Средняя стоимость работ': ''
              }
    try:
        myDict['Наименование'] = (tel[0]['name'])
    except:
        pass
    try:
        myDict['Сайт HOUZ'] = value
        myDict['Сайт'] = (tel[0]['url'])
    except:
        pass
    try:
        myDict['Номер телефона'] = (tel[0]['telephone'])
    except:
        pass
    try:
        myDict['Адрес'] = (tel[0]['address']['addressLocality'] + ' ' + tel[0]['address']['postalCode'])
    except:
        try:
            avgCost = soup.findAll('div', 'sc-183mtny-0 Row___StyledBox-sc-1xmq8tu-0 jqaQXH kwUbop')
            myDict['Адрес'] = avgCost[1].text
        except:
            pass
        pass
    try:
        myDict['О нас'] = (tel[0]['description'])
    except:
        pass
    try:
        myDict['Предоставляемые услуги'] = (tel[0]['hasOfferCatalog']['name'])
    except:
        pass
    try:
        myDict['География работ'] = (tel[0]['areaServed']['name'])
    except:
        pass
    try:
        myAvg = soup.findAll('div', 'sc-183mtny-0 Row___StyledBox-sc-1xmq8tu-0 jqaQXH kwUbop')
        myDict['Средняя стоимость работ'] = myAvg[2].text
    except:
        pass
    myArray.append(myDict)
    return myArray

mass = []
def getLinks(value):
    global mass
    global spec
    global index
    config = configparser.ConfigParser()
    config.read('MyData.ini')
    spec = config['Link']['spec']
    index = '/c/' + config['Link']['index']
    mass = []
    print(url + spec + index)
    response = requests.get(url + spec + index + '/p/' + str(value))
    soup = BeautifulSoup(response.text, 'html.parser')
    s = soup.find('ul', 'hz-pro-search-results').findAll('a', 'hz-pro-ctl')
    for item in s:
        mass.append(item.get('href'))


def getNumberOfPages():
    global spec
    global index
    config = configparser.ConfigParser()
    config.read('MyData.ini')
    spec = config['Link']['spec']
    index = '/c/' + config['Link']['index']
    print(url+spec+index)
    response = requests.get(url + spec + index)
    soup = BeautifulSoup(response.text, 'html.parser')
    s = soup.find('div', 'hz-pro-search-controls__pagination mlm').findAll('span', 'text-bold')
    numAll = ''
    numOne = ''
    numZero = ''
    for symbol in s[0].text:
        if (symbol != "\xa0" and symbol != ' '):
            numZero += symbol
    for symbol in s[1].text:
        if (symbol != "\xa0" and symbol != ' '):
            numOne += symbol
    for symbol in s[2].text:
        if (symbol != "\xa0" and symbol != ' '):
            numAll += symbol
    print(numAll + ' ' + numOne + ' ' + numZero)
    return (int(numAll) / ((int(numOne) - int(numZero)) + 1))


def end_func():
    df = pd.DataFrame(data=myArray)
    df.to_excel('output.xlsx', index=False)


def arrLinks():
    with ThreadPoolExecutor(max_workers=100000) as t:
        t.map(Parser, mass)
    print(myArray)
    end_func()

def start():
    try:
        numberOfPages = getNumberOfPages()
    except Exception:
        print("Ничего не найдено")
        return 1
    arr = []
    i = 0
    while (i < numberOfPages * 15):
        arr.append(i)
        i += 15
    with ThreadPoolExecutor(max_workers=10000) as p:
        p.map(getLinks, arr)
    arrLinks()
    print(mass)
    return 0

'''if __name__ == "__main__":
    start()'''