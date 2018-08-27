# -*- coding: utf-8 -*-
import scrapy
from imdbscrape.items import MovieItem

class MovieSpider(scrapy.Spider):
	name = 'movie'
	allowed_domains = ['imdb.com']
	start_urls = ['https://www.imdb.com/search/title?year=2017,2018&title_type=feature&sort=moviemeter,asc']

	def parse(self, response):
		urls = response.css('h3.lister-item-header > a::attr(href)').extract()
		for url in urls:
			yield scrapy.Request(url=response.urljoin(url),callback=self.parse_movie)

		nextpg = response.css('div.desc > a::attr(href)').extract_first()
		if nextpg:
			nextpg = response.urljoin(nextpg)
			yield scrapy.Request(url=nextpg,callback=self.parse)

	def parse_movie(self, response):
		item = MovieItem()
		item['title'] = self.getTitle(response)
		item['year'] = self.getYear(response)
		item['rating'] = self.getRating(response)
		item['genre'] = self.getGenre(response)
		item['director'] = self.getDirector(response)
		item['summary'] = self.getSummary(response)
		item['actors'] = self.getActors(response)
		yield item

	def getTitle(self, response):
		value = response.css('div.title_wrapper > h1::text').extract_first()
		if value:
			return value.replace(u'\xa0',u'')
		return 'NA'

	def getYear(self, response):
		value = response.css('span#titleYear > a::text').extract_first()
		if value:
			return value
			return 'NA'

	def getRating(self, response):
		value = response.css('div.ratingValue > strong > span::text').extract_first()
		if value:
			return value
		return 'UNRATED'

	def getGenre(self, response):
		data = response.css('div.subtext > a::text').extract()
		if data:
			data.pop()
			return data
		return 'NA'

	def getDirector(self, response):
		data  = response.css('div.credit_summary_item')
		if data:
			value = data[0].css('a::text').extract_first()
			if value:
				return value
		return 'NA'

	def getActors(self, response):
		data  = response.css('div.credit_summary_item')
		if data:
			value = data[-1].css('a::text').extract()
			if value:
				if len(value)!=1:
					value.pop()
				return value
		return 'NA'

	def getSummary(self, response):
		data = response.css('div.summary_text::text').extract_first()
		if data:
			data = data.lstrip().rstrip()
			return data;
		return 'NA'
