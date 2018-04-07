# -*- coding: utf-8 -*-
import scrapy
#导入链接规则匹配类，用来提取符合规则的连接
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TencentSpider.items import TencentItem

"""
   爬取腾讯社会招聘列表页
"""
class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?start=0#a']
    # Response里链接的提取规则
    pagelink = LinkExtractor(allow=("start=\d+"))
    rules = (
        # 获取这个列表里的链接，依次发送请求，并且继续跟进，调用指定回调函数处理
        Rule(pagelink, callback='parseTencent', follow=True),
    )

    # 指定的回调函数
    def parseTencent(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = TencentItem()
            item['positionName'] = each.xpath("./td[1]/a/text()").extract()[0] #if len(each.xpath("./td[1]/a/text()").extract()) > 0 else ''
            item['positionLink'] = "https://hr.tencent.com/" + each.xpath("./td[1]/a/@href").extract()[0] #if len(each.xpath("./td[1]/a/@href").extract()) > 0 else ''
            item['positionType'] = each.xpath("./td[2]/text()").extract()[0] if len(each.xpath("./td[2]/text()").extract()) > 0 else ''
            item['peopleNum']    = each.xpath("./td[3]/text()").extract()[0] #if len(each.xpath("./td[3]/text()").extract()) > 0 else ''
            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0] #if len(each.xpath("./td[4]/text()").extract()) > 0 else ''
            item['publishTime']  = each.xpath("./td[5]/text()").extract()[0] #if len(each.xpath("./td[5]/text()").extract()) > 0 else ''

            yield item