import scrapy
from urllib.parse import unquote
import re
from random import randint
from time import sleep


class HotelSpider(scrapy.Spider):
    name = 'hotels'
    start_urls = [
        'https://booking.com/searchresults.it.html?aid=356980&label=gog235jc-1DCAYYrwIocUITdHJlbnRpbm8tYWx0ZS1hZGlnZUgUWANocYgBAZgBFLgBF8gBD9gBA-gBAfgBAogCAagCA7gCsYyR7gXAAgE&sid=c408e71d92ef3b7d5f94e5afd51b3287&tmpl=searchresults&class_interval=1&dest_id=911&dest_type=region&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&region=911&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=region&src_elem=sb&srpvid=f11d9ff8fc06022d&ss=Trentino-Alto%20Adige&ss_all=0&ssb=empty&sshis=0&ssne=Trentino-Alto%20Adige&ssne_untouched=Trentino-Alto%20Adige&top_ufis=1&rows=25&offset=',

    ]

    offset = 25
    base_url = 'https://www.booking.com'
    desired_services = ['Animali', 'Parcheggio', 'Internet', 'Servizi benessere', 'Servizi di ristorazione']

    def start_requests(self):
        total_offset = self.offset * int(self.page)
        self.logger.info(self.page)
        self.logger.info(total_offset)
        for url in self.start_urls:
            yield scrapy.Request(url+str(total_offset), dont_filter=True)

    def parse(self, response):
        self.logger.info('here')
        for hotel in response.css('div.sr_item.sr_item_new.sr_item_default.sr_property_block'):
            link = hotel.css('a.hotel_name_link.url::attr(href)').get()

            absolute_url = self.base_url + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        type = response.xpath('//h2[@id="hp_hotel_name"]/span/text()').get()
        name = response.css('h2.hp__hotel-name::text').extract()
        address = response.css('span.hp_address_subtitle.js-hp_address_subtitle.jq_tooltip::text').get()
        pos = response.xpath('//a[@id="hotel_address"]/@data-atlas-latlng').extract()
        pos = pos[0].split(',')

        checkin_from = response.xpath('//div[@id="checkin_policy"]/p/span[@class="u-display-block"]/@data-from').get()
        checkin_to = response.xpath('//div[@id="checkin_policy"]/p/span[@class="u-display-block"]/@data-until').get()

        checkout_from = response.xpath('//div[@id="checkout_policy"]/p/span[@class="u-display-block"]/@data-from').get()
        checkout_to = response.xpath('//div[@id="checkout_policy"]/p/span[@class="u-display-block"]/@data-until').get()

        name[1] = str(name[1].replace('\n', ''))

        address = str(address.replace('\n', ''))

        paragraphs = response.xpath('//div[@id="property_description_content"]')
        paragraphs = paragraphs.css('p::text').extract()
        description = ''
        for p in paragraphs:
            description += p + '\n'

        score = response.xpath('//div[@class="bui-review-score__badge"]/text()').get()

        num_reviews = response.xpath('//div[@class="bui-review-score__text"]/text()').get()
        num_reviews = re.findall(r'[0-9]+', num_reviews)
        if num_reviews:
            num_reviews = num_reviews[0]
        else:
            num_reviews = 0

        services = {
            'Animali': False,
            'Parcheggio': False,
            'Internet': False,
            'Servizi benessere': False,
            'Servizi di ristorazione': False
        }
        for s in response.css('div.facilitiesChecklistSection'):
            service_title = s.css('h5::text').extract()
            service_title[1] = str(service_title[1].replace('\n', ''))
            service_title[1] = service_title[1]
            if service_title[1] in services:
                if service_title[1] == "Animali":
                    policy = s.xpath('//li[@class="policy"]/p/text()').get()
                    policy = policy.split()
                    if "non" not in policy:
                        services[service_title[1]] = True
                elif service_title[1] == "Internet" or service_title[1] == "Parcheggio":
                    free = s.xpath('//li[@class="policy"]/p/span/text()').get()
                    if free == 'Gratis!':
                        services[service_title[1]] = True
                else:
                    services[service_title[1]] = True

        rmv = re.findall(r"[(].*[)]", address)
        if len(rmv) > 0:
            address = address.replace(rmv[0], '')

        hotel = {
            'name': name[1].strip(),
            'type': type.strip(),
            'address': address,
            'lat': pos[0],
            'lon': pos[1],
            'checkin_from': checkin_from,
            'checkin_to': checkin_to,
            'checkout_from': checkout_from,
            'checkout_to': checkout_to,
            'description': description,
            'score': score.strip(),
            'num_reviews': num_reviews.strip()
        }

        for service in services:
            hotel.update({service: services[service]})
        return hotel
