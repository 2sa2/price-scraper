from abc import ABC, abstractmethod

sites = []
# 9999 represents out-of-stock
def call_correct_get_price(site, soup):
    if site == sites[0]:
        site0 = Site0(soup)
        if site0.in_stock():
            return site0.get_price()
        return 9999
    elif site == sites[1]:
        site1 = Site1(soup)
        if site1.in_stock():
            return site1.get_price()
        return 9999
    elif site == sites[2]:
        site2 = Site2(soup)
        if site2.in_stock():
            return site2.get_price()
        return 9999
    else:
        site3 = Site3(soup)
        return site3.get_price()


class PartSource(ABC):
    def __init__(self, soup):
        self.soup = soup
        super().__init__()

    @abstractmethod
    def get_price(self):
        try:
            item_id = self.soup.find(attrs={'name': 'product'})['value']
            price = self.soup.find('span', {'id': 'product-price-' + item_id}).text.strip()[1:]
            return price
        except:
            print('html changed (item possibly no longer available)')
            return 8888

    @abstractmethod
    def in_stock(self, html):
        if html is not None:
            return True
        return False


class Site0(PartSource):
    def get_price(self):
        return super().get_price()

    def in_stock(self):
        stock_tag = self.soup.find(attrs={'class': 'availability in-stock pull-right'})
        return super().in_stock(stock_tag)


class Site1(PartSource):
    def get_price(self):
        return super().get_price()

    def in_stock(self):
        stock_tag = self.soup.find(attrs={'class': 'availability in-stock'})
        return super().in_stock(stock_tag)


class Site2(PartSource):
    def get_price(self):
        return self.soup.find('div', {'class': 'price'}).text.strip()[3:]

    def in_stock(self):
        return True


class Site3(PartSource):
    def get_price(self):
        try:
            price = self.soup.find('span', {'id': 'prcIsum'}).text.strip()[4:].replace(',', '')
            if price[-3:] == '/ea':
                price = price[:-3]
            return price
        except:
            print('html changed (item possibly no longer available)')
            return 8888

    # TODO
    def in_stock(self):
        return True
