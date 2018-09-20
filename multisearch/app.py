#!/usr/bin/env python
import argparse
import sys
from collections import defaultdict

from requests.exceptions import ConnectionError

from zeep import Client

# encoding: utf-8




wsdl = 'http://webapi.allegro.pl/uploader.php?wsdl'
wsdl = 'https://webapi.allegro.pl/service.php?wsdl'

client = Client(wsdl)

# version = client.service.doQuerySysStatus(1, 1, apikey)
# print(version)


class Item():
    item_id = None
    title = None
    url = None
    price = None
    price_w_shipping = None
    user_id = None
    user_login = None

    def __init__(self, data):
        self.title = data['itemTitle']
        self.url = 'http://allegro.pl/show_item.php?item=%s' % data['itemId']

        self.price = data['priceInfo']['item'][0]['priceValue']
        self.price_w_shipping = data['priceInfo']['item'][1]['priceValue']

        # print(data['sellerInfo'])
        if data['sellerInfo']:
            self.user_id = data['sellerInfo']['userId']
            self.user_login = data['sellerInfo']['userLogin']

    def display(self):
        print("Title: %s" % self.title)
        print("Url: %s" % self.url)

        print("Price: %s / %s" % (self.price, self.price_w_shipping))
        print("User Login: %s" % self.user_login)
        print('---')


class MultiSearch():
    lists = []
    webapi_key = None

    def __init__(self, api_key):
        self.webapi_key = api_key

    def append(self, items):
        self.lists.append(items)

    def make_filter(self, query):
        return {
            'item': [{
                'filterId': k,
                'filterValueId': {
                    'item': v
                }
            } for k, v in query.items()]
        }

    def fetch_results(self, filter):
        '''
        http://allegro.pl/webapi/documentation.php/show/id,1342
        '''
        res = client.service.doGetItemsList(webapiKey=self.webapi_key,
                                            countryId=1,
                                            filterOptions=self.make_filter(filter),
                                            resultScope=3)

        self.items_count = res['itemsCount']
        self.featured_count = res['itemsFeaturedCount']

        items = tuple()
        if res['itemsList']:
            items = (Item(item_data) for item_data in res['itemsList']['item'])

        self.append(items)
        return items

    def match_uid(self):
        groups = {}

        for idx, item_list in enumerate(self.lists):
            if not item_list:
                return []

            for item in item_list:
                if item.user_id:
                    if item.user_id not in groups:
                        groups[item.user_id] = defaultdict(list)

                    groups[item.user_id][idx].append(item)

        result = {}
        for uid, ldict in groups.items():
            # ldict is a {idx: items_list, ...} structure
            #
            # if user has item from all lists
            if len(ldict) == len(self.lists):
                result[uid] = [item for sublist in ldict.values() for item in sublist]

        return result


def load_api_key():
    try:
        with open('./api_key', 'r') as f:
            return f.read().strip()
    except Exception:
        print("You have to create a 'api_key' file with the allegro api key inside", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Allegro MultiSearch.')
    parser.add_argument('query', metavar='N', type=str, nargs='+', action='append',
                        help='Query strings to search')
    args = parser.parse_args()

    app = MultiSearch(api_key=load_api_key())

    try:
        print('Queries:', args.query[0])

        for query in args.query[0]:
            app.fetch_results({'search': query})

        print('\nResults:')
        items = app.match_uid()
        if not items:
            print('No results')
            sys.exit(0)

        for uid, items in items.items():
            print('\n---%s---\n' % uid)

            [item.display() for item in items]
    except ConnectionError as e:
        print('Connection error: %s ' % e, file=sys.strerr)
    except Exception as e:
        print('Error: %s ' % e, file=sys.strerr)
        import traceback
        traceback.print_exc()
