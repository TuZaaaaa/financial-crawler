

from db.sql_helper import SqlHelper
from word_cloud_generate import WordCloudGenerate

db = SqlHelper()

res = db.get_list('select * from crawler_tb1', [])

print(res)
contents = ''
for r in res:
    contents += r['content']

wcg = WordCloudGenerate(contents, 'wordcloud.png')
result = wcg.run()
print(result)

