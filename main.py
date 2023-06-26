import requests as rq
import pandas as pd

# http://free-proxy.cz/ru/proxylist/country/all/http/ping/all

def respons_catalog():

    url = 'https://catalog.wb.ru/sellers/catalog?appType=1&curr=rub&dest=-4016353&regions=80,38,4,64,83,33,68,70,69,30,86,40,1,66,110,22,31,48,114&sort=popular&spp=25&supplier=1160557'
    headers = {
    'Accept':'*/*' ,
    'Accept-Language':'ru,en;q=0.9' ,
    'Connection':'keep-alive' ,
    'Origin': 'https://www.wildberries.ru' ,
    'Referer': 'https://www.wildberries.ru/catalog/muzhchinam/odezhda/bryuki-i-shorty',
    'Sec-Fetch-Dest': 'empty' ,
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.0.2285 Yowser/2.5 Safari/537.36' ,
    'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0' ,
    'sec-ch-ua-platform': '"macOS"'
            }
    response = rq.get(url=url,headers=headers)

    return response.json()
def respons_item(url):

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/muzhchinam/odezhda/bryuki-i-shorty',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.0.2285 Yowser/2.5 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    response = rq.get(url=url, headers=headers)

    return response.json()

def prepare_items(respons):
    products = []

    products_raw = respons.get('data', {}).get('products',None)

    if products_raw!= None and len(products_raw) > 0 :
        for product in products_raw:
            products.append({
                'id': product.get('id', None),
                'root': product.get('root', None)
            })

    return products

def prepare_items_item(respons):
    products = []

    products_raw = respons.get('data', {}).get('products',None)

    if products_raw != None and len(products_raw) > 0 :
        for product in products_raw:
            sizeList = product.get('sizes',None)
            for size in sizeList:
                if size.get('stocks') == []:
                    products.append({
                        'origName': f"{size.get('origName',None)} ({size.get('name',None)})",
                        'id': product.get('id',None),
                        'colors': product.get('colors',None)[0].get('name',None),
                        'name': product.get('name',None)
                    })

    return products

def main():

    catalogs = respons_catalog()
    products_catalog= prepare_items(catalogs)

    res_sort = []

    #Собираю все root в одном списке
    for i in products_catalog:
        res_sort.append(i['root'])

    #Удаляю повторяющиеся root
    res_set = set(res_sort)
    res_dict = {}

    #Добавляю в словарь res_dict {root:[]}
    for i in res_set:
        res_dict[i] = []

    #В словаре сверху для каждого root обавляю значения принадлежащие ему
    for i in products_catalog:
        res_dict.setdefault(i['root'], []).append(str(i['id']))

    #url = 'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-4016353&regions=80,38,4,64,83,33,68,70,69,30,86,40,1,66,110,22,31,48,114&spp=25&nm=160891306;160890241;153306130;153306134;160889977;153306132;153306131'

    with open('products.csv', 'w', encoding='utf8') as _:
        for _,value in res_dict.items():
            resopons = respons_item(f'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-4016353&regions=80,38,4,64,83,33,68,70,69,30,86,40,1,66,110,22,31,48,114&spp=25&nm={";".join(value)}')
            products = prepare_items_item(resopons)
            pd.DataFrame(products).to_csv('products.csv', encoding='utf8', mode='a', index=False)


if __name__ == '__main__':
    main()
