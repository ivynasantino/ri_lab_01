# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('seeds/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        #
        # inclua seu código aqui
        #

        for href in response.css("div.eltdf-pt-one-item a::attr(href)"):
            print(href)
            yield response.follow(href, self.parse_post, meta = {'url': response.url})
        
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
    
    def parse_post(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'category': extract_with_css("a.category tag::text"),
            'title': extract_with_css("h3.eltdf-pt-one-title::text"),
        }
