import requests
import csv
from datetime import datetime


def function():

    response = requests.get('https://search.wb.ru/exactmatch/ru/common/v4/'
                            'search?appType=1&curr=rub&dest=-3155928&query='
                            'iphone%2013%20mini&regions=80,64,38,4,115,83,33,68,70,69,30,86,40,1,66,48,'
                            '110,31,22,114&resultset=catalog&sort=popular&spp=15&suppressSpellcheck=false')

    response_dict = response.json()
    response_list = response_dict['data']['products']

    list_of_products = []
    dict_of_product = {}

    for product in response_list:
        dict_of_product.update({'Название': product['name']})
        dict_of_product.update({'Цвет': product['colors'][0]['name']})
        dict_of_product.update({'Цена': int(product['priceU'])/100})
        dict_of_product.update({'Цена со скидкой': int(product['salePriceU'])/100})
        dict_of_product.update({'Айди товара': product['id']})

        list_of_products.append(dict_of_product)
        dict_of_product = {}

    return list_of_products


def write_file(rows):
    fieldnames = ['Название', 'Цвет', 'Цена', 'Цена со скидкой', 'Айди товара']
    with open(f'C:/Users/Bulatshuh/wildberries/temp/{str(datetime.now().strftime("%d-%m-%Y--%H.%M.%S"))}'
              f'_products_file.csv',
              'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(rows)


def get_bargain(products):
    list_of_sales_amount = []

    for product in products:
        sale_amount = float(product['Цена']) - float(product['Цена со скидкой'])
        list_of_sales_amount.append(sale_amount)

    bargain_amount = max(list_of_sales_amount)
    bargain_number = list_of_sales_amount.index(bargain_amount)

    # print(f'Самая большая скидка - {bargain_amount}\nУ товара:\n{products[bargain_number]}\n')

    fieldnames = ['Название', 'Цвет', 'Цена', 'Цена со скидкой', 'Айди товара']
    with open(f'C:/Users/Bulatshuh/wildberries/temp/{str(datetime.now().strftime("%d-%m-%Y--%H.%M.%S"))}'
              f'_bargain_product.csv',
              'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow('')
        writer.writerow([f'Самая большая скидка - {bargain_amount}'])
        writer.writerow(['Данные товара:'])

        product_writer = csv.DictWriter(file, fieldnames=fieldnames)
        product_writer.writeheader()
        product_writer.writerow(products[bargain_number])

    list_of_prices = []

    for product in products:
        price = float(product['Цена со скидкой'])
        list_of_prices.append(price)

    cheapest_price = min(list_of_prices)
    item_number = list_of_prices.index(cheapest_price)

    # print(f'Самая низкая цена - {cheapest_price}\nУ товара:\n{products[item_number]}')

    fieldnames = ['Название', 'Цвет', 'Цена', 'Цена со скидкой', 'Айди товара']
    with open(f'C:/Users/Bulatshuh/wildberries/temp/{str(datetime.now().strftime("%d-%m-%Y--%H.%M.%S"))}'
              f'_cheapest_product.csv',
              'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow('')
        writer.writerow([f'Самая низкая цена - {cheapest_price}'])
        writer.writerow(['Данные товара:'])

        product_writer = csv.DictWriter(file, fieldnames=fieldnames)
        product_writer.writeheader()
        product_writer.writerow(products[item_number])


if __name__ == '__main__':
    write_file(function())
    get_bargain(function())
