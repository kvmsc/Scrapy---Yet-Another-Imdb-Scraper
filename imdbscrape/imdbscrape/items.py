# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
	year = scrapy.Field()
	title = scrapy.Field()
	rating = scrapy.Field()
	genre = scrapy.Field()
	director = scrapy.Field()
	actors = scrapy.Field()
	summary = scrapy.Field()