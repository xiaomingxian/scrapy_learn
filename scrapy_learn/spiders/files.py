import os
import json

if __name__ == '__main__':
    # file_data = open("/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/links_pure.txt")

    county = len(
        open('/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/file30/18.txt', 'rU').readlines())

    sumy=0
    sumd=0
    for i in range(0, 32):
        county = len(
            open('/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/file30/' + str(i) + '.txt',
                 'rU').readlines())

        count = len(open('/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/res/' + str(i),
                         'rU').readlines())
        sumy+=county
        sumd+=count
        if county != count:
            print(i, county, count)
            # 找出url
            # 解析结果的每一行 找出不在 数据源中的url
            file_data = open(
                "/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/file30/" + str(i) + ".txt")
            res = open('/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/res/' + str(i))

            datay = {}
            #

            urls = {}
            num = 1
            while True:
                text = res.readline()  # 只读取一行内容
                data = text.replace('\n', '') \
                    .replace('\\', '') \
                    .replace('\\xa0', '') \
                    .replace('"', '\'') \
                    .replace('\',', '",') \
                    .replace('\'}', '"}') \
                    .replace('{\'', '{"') \
                    .replace(', \'', ', "') \
                    .replace('\':', '":') \
                    .replace(': \'', ': "')
                # print('----data:::', data)
                # 判断是否读取到内容
                if not text:
                    break
                obj = json.loads(data)
                # print(obj['url'], '   ', num)
                urls[obj['url']] = 'xxx'
                num = num + 1

            while True:
                text = file_data.readline()  # 只读取一行内容
                url = text.replace('\n', '')
                # 判断是否读取到内容
                if not text:
                    break
                try:
                    urls[url]
                except Exception as e:
                    print('---没结果的url::', url)
                    ff = open(
                        "/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/fail_urls/fail_url",
                        'a')
                    ff.write(url + '\n')
                    ff.close()

            pass

        print(i, count)
    print(sumy,sumd)
    # 查出来没有记录的url

    # print(county, count)
    # index = 0
    # file_index = 0
    # file_suf = "/Users/xxm/develop/py_workspace/scrapy_learn/scrapy_learn/spiders/files/filesMore/"
    # file = file_suf + '0.txt'
    # # os.mknod(file)
    #
    # while True:
    #     if index % 5000 == 0 and index!=0:
    #         file_index = file_index + 1
    #         print('============+>>>>>>>>>>>>>>>>>>>>>>>>>  新建文件：：：：',file_index)
    #         file = file_suf + str(file_index) + '.txt'
    #         # os.mknod(file)
    #     text = file_data.readline()  # 只读取一行内容
    #     # 判断是否读取到内容
    #     if not text:
    #         break
    #     # self.start_urls.append(text)
    #     f = open(file, 'a')
    #     f.write(text)
    #     f.close()
    #
    #     url = text.replace('\n', '')
    #     index = index + 1
    #     print(url)
