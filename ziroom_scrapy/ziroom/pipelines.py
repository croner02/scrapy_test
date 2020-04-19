# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import csv
from scrapy.exceptions import DropItem


class ZiroomPipeline(object):

    def open_spider(self, spider):
        self.filename = open('ziroom.csv', 'w', encoding='utf-8-sig', newline="")
        self.writer = csv.DictWriter(self.filename, fieldnames=['title', 'href', 'desc', 'location', 'price'])
        self.writer.writeheader()

    def write_csv(self, item, spider):
        if item['title']:
            self.writer.writerow(dict(item))
        else:
            raise DropItem('Missing title i %s' % item)

    def process_item(self, item, spider):
        self.write_csv(item, spider)
        return item

    def close_spider(self, spider):
        self.filename.close()


class ZiroomPipelineJson(object):

    def open_spider(self, spider):
        self.filename = open('ziroom.json', 'w', encoding='utf-8')

    def write_json(self, item):
        if item['title']:
            line = json.dumps(dict(item), ensure_ascii=False)
            self.filename.write(line + '\n')
        else:
            raise DropItem('Missing title i %s' % item)

    def process_item(self, item, spider):
        self.write_json(item)

    def close_spider(self, spider):
        self.filename.close()
