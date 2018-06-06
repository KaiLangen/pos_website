import django
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_website.settings')
django.setup()
from dashboard.models import Customer
from pos_scrapy.metrics import calculate_metrics

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('gomjfreeway')
    process.start()

    for cust in Customer.objects.all():
        calculate_metrics(cust)
