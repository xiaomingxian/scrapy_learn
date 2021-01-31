import os
import json

if __name__ == '__main__':
    file_data = open("/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/links_pure.txt")
    fails = open("/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/fail_urls/fail_url.txt")




    fail={}
    while True:
        text = fails.readline()  # 只读取一行内容
        url = text.replace('\n', '')
        # 判断是否读取到内容
        if not text:
            break
        fail[url]='xxxx'

    i=1
    while True:
        text = file_data.readline()  # 只读取一行内容
        url = text.replace('\n', '')
        # 判断是否读取到内容
        if not text:
            break
        try:
           print(url, fail[url],i)
           i+=1
        except Exception as e:
            # print(e)
            pass


