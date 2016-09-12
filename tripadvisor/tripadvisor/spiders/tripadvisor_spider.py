import scrapy
from tripadvisor.items import TripadvisorItem

class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com']
    start_urls = (
        'https://www.tripadvisor.com/Restaurants-g60974-Buffalo_New_York.html',
    )

    def parse(self, response):
        # process each restaurant link
        urls = response.xpath('//h3[@class="title"]/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_restaurant)
            yield request

        # process next page
        next_page_url = response.xpath('//a[text()="Next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_restaurant(self, response):
        item = TripadvisorItem()
        item['name'] = response.xpath(
            '//div[@class="mapContainer"]/@data-name').extract_first()
        item['rating'] = response.xpath(
            '//img[@property="ratingValue"]/@content').extract_first()
        item['latitude'] = response.xpath(
            '//div[@class="mapContainer"]/@data-lat').extract_first()
        item['longitude'] = response.xpath(
            '//div[@class="mapContainer"]/@data-lng').extract_first()            
        item['url'] = response.url
        yield item

        


      

