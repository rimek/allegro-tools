from collections import defaultdict

from zeep import Client


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

    client = Client('https://webapi.allegro.pl/service.php?wsdl')

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
        res = self.client.service.doGetItemsList(webapiKey=self.webapi_key,
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
