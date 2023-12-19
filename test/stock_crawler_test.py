from stock_crawler import StockCrawler

sc = StockCrawler(['https://company.cnstock.com/company/scp_gsxw/1', 'https://ggjd.cnstock.com/company/scp_ggjd/tjd_bbdj', 'https://ggjd.cnstock.com/company/scp_ggjd/tjd_ggkx', 'https://jrz.cnstock.com/'], 1)
result = sc.run()
print(result)