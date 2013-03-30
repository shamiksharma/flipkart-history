import json
from scrapy.spider import BaseSpider, Request
from scrapy.item import Item, Field


class Book_Product(Item):
    """
    Describes a book item in flipkart.com
    """
    title = Field()
    subtitle = Field()
    uid = Field()
    fsp = Field()
    mrp = Field()


class Flipkart_Spider(BaseSpider):
    name = "flipkart"
    allowed_domains = ["flipkart.com"]
    start_urls = [
        "http://www.flipkart.com/m/store/buk/loadmore?store=buk&start=1"
    ]

    count = 1
    items = []

    def parse(self, response):
        data = json.loads(response.body)['result']['products'].values()
        for i in data:
            item = Book_Product()
            item['title'] = i['title']
            item['subtitle'] = i['subtitle']
            item['uid'] = i['permanentProductPageUrl'].split('/')[-1].split('?')[0]
            item['fsp'] = i['fsp']
            item['mrp'] = i['mrp']
            self.items.append(item)
        print len(self.items)
        self.count += 10
        if self.count > 100:
            # < Python 3.3 doesn't allows mixing of return and yield statements in same function.
            # So, we yield another method self.return_data which then returns the result.
            yield Request("http://www.flipkart.com/m/store/buk/loadmore?store=buk&start=%d" % self.count, self.return_data)
        yield Request("http://www.flipkart.com/m/store/buk/loadmore?store=buk&start=%d" % self.count, self.parse)

    def return_data(self, _):
        return self.items