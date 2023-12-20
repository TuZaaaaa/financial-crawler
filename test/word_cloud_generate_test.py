

from db.sql_helper import SqlHelper
from word_cloud_generate import WordCloudGenerate

db = SqlHelper()

res = db.get_list('select * from crawler_tb3', [])

print(res)
contents = ''
for r in res:
    contents += r['content']

wcg = WordCloudGenerate(contents, '../picture/wordcloud.png')
result = wcg.run()
print(result)

