import scrapy

from scrapy.loader import ItemLoader
from ..items import ManobankItem
from itemloaders.processors import TakeFirst


class ManobankSpider(scrapy.Spider):
	name = 'manobank'
	start_urls = ['https://mano.bank/naujienos']

	def parse(self, response):
		post_links = response.xpath('//div[@class="bottom-link"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="blog-content"]/h2/text()').get()
		description = response.xpath('//div[@class="blog-vidinis-text"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="blog-content"]/p/text()').get()

		item = ItemLoader(item=ManobankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
