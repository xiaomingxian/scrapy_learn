if __name__ == '__main__':
    fs = open('/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/links_pure.txt')
    obj = {}
    num = 0
    while True:
        text = fs.readline()  # 只读取一行内容
        data = text.replace('\n', '')
        try:
            res = obj[data]
            if res: num += 1
        except Exception as e:
            print(data)
        obj[data] = 'xxxxx'
        if not text:
            break
    print(num)
