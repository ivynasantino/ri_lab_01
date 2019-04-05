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
       
        div_principal = "div.eltdf-container-inner a::attr(href)"
        for href in response.css(div_principal):
            print(href)
            yield response.follow(href, self.parse_post, meta = {'url': response.url})
        
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
    
    def parse_post(self, response):
        def extract_with_css(query):
            '''
            '''
            return response.css(query).get(default='').strip()

        def extract_with_css_all(query):
            '''
            '''
            return response.css(query).getall()

        yield {
            'categoria': extract_with_css("div.eltdf-post-info-category > a::text"),
            'titulo': extract_with_css("a.eltdf-pt-link::text"),
            'subtitulo': extract_with_css("div.wpb_wrapper > h3::text"),
            'url': response.url,
            'autor': extract_with_css("a.eltdf-post-info-author-link::text"),
            'data': extract_with_css("div.eltdf-post-info-date > a::text"),
            'texto': extract_with_css_all("div.eltdf-post-text-inner > a::text, div.eltdf-post-text-inner > p::text")
        }
