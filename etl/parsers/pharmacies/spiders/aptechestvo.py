import scrapy
from ..items import AptechestvoItem


class FarmaniSpider(scrapy.Spider):
    name = "aptechestvo"

    def start_requests(self):
        urls = [
            'https://aptechestvo.ru/catalog/lekarstva_i_bady/?PAGEN_2=1'
        ]
        yield scrapy.Request(url=urls[0], callback=self.get_pages)

    def get_pages(self, response):
        max_page = response.css("a.dark_link::text").getall()[-1]
        for page in range(1, int(max_page)+1):
            yield scrapy.Request(url=f'https://aptechestvo.ru/catalog/lekarstva_i_bady/?PAGEN_2={page}',
                                 callback=self.parse_page)

    def parse_page(self, response):
        print("START")
        for i in range(1, 20):
            header = response.xpath(f"/html/body/section[3]/div[2]/div[4]/div[2]/div[1]/div[{i}]/div/div[3]/a/text()").getall()[0].strip()
            print("HEADER", header)
            price = response.xpath(f"/html/body/section[3]/div[2]/div[4]/div[2]/div[1]/div[{i}]/div/div[6]/div[1]/text()").getall()[0].strip()
            print("PRICE", price)
            try:
                response.xpath(f"/html/body/section[3]/div[2]/div[4]/div[2]/div[1]/div[{i}]/div/div[6]/div[1]/").getall()
                is_prescription = True
            except ValueError:
                is_prescription = False
            print("is_prescription", is_prescription)
            img_src = 'https://aptechestvo.ru' + response.xpath(f"/html/body/section[3]/div[2]/div[4]/div[2]/div[1]/div[{i}]/div/div[2]/a/img/@src").getall()[0].strip()
            print("img_src", img_src)
            print("END")
            object = AptechestvoItem(header=header, price=price, is_prescription=is_prescription, img_src=img_src)
            yield object
