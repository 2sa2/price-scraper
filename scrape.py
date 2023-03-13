# created by et2 on May 10, 2018

import requests
from bs4 import BeautifulSoup
from pyexcel_ods3 import save_data, get_data
from collections import OrderedDict
from time import sleep
from random import randint
import get_part_prices as prices
import change_file_names
import timeit

file_location = ''
file = 'price-sheet.ods'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}


# ods = [keys, data]
def process_hyperlinks(ods):
    # for each sheet
    for key in ods[0]:
        for row in range(0, len(ods[1][key])):
            for col in range(0, len(ods[1][key][row])):
                if type(ods[1][key][row][col]) == str and ods[1][key][row][col][:5] == 'https':
                    print(ods[1][key][row][col])
                    site = get_store(ods[1][key][row][col])
                    try:
                        price = prices.call_correct_get_price(
                            site, get_html(request_url(ods[1][key][row][col])))
                        # get rid of following if statement once sheet is formatted properly (each part has
                        # a 'qty' line)
                        if ods[1][key][row + 1][0] == 'qty':
                            ods[1][key][row - 1][col] = round(float(price) / float(ods[1][key][row + 1][col]), 2)
                        else:
                            ods[1][key][row - 1][col] = float(price)
                    except:
                        print('something went wrong')
    return ods


def read_ods(file_name):
    data = get_data(file_name)
    keys = data.keys()
    return [keys, data]


def write_ods(updated_data):
    data = OrderedDict()
    data.update(updated_data)
    save_data(file_location, data)


def request_url(url):
    try:
        sleep(1)
        return requests.get(url, headers=headers)
    except ConnectionError:
        print('request failed: ' + url)


# returns domain name without top level domain
def get_store(address):
    site = address.split('.')[1]
    return site


def get_html(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except:
        print("get html failed")


# ods = [keys, data]
def get_best_price_product(ods):
    for key in ods[0]:
        for row in range(0, len(ods[1][key])):
            if len(ods[1][key][row]) > 1 and type(ods[1][key][row][1]) != str and ods[1][key][row][0] != 'qty':
                try:
                    min_in_row = min(ods[1][key][row][1:])
                    # min_in_row_index = ods[1][key][row].index(min_in_row)
                    ods[1][key][row + 1][0] = min_in_row
                except:
                    print('best price not found for: ' + key + ' ' + ods[1][key][row][0])
    return ods


def main():
    start = timeit.default_timer()
    ods_dict = read_ods(file)
    d = process_hyperlinks(ods_dict)
    d = get_best_price_product(d)
    change_file_names.change_name(file_location + '/price-scraper/price-sheets/price-sheet-recent.ods')
    write_ods(d[1])
    stop = timeit.default_timer()
    seconds = stop - start
    minutes = 0
    if float(seconds) > 59:
        minutes = int(seconds / 60)
        seconds %= 60
    print(str(minutes) + ' minutes and ' + str(format(seconds, '.2f')) + ' seconds ')


if __name__ == '__main__':
    main()
