import redis
import time

r = redis.Redis(host="localhost", port=6379, db=0)


def main():
    for i in range(1,100000):
        with r.pipeline(transaction=False) as p:
            p.sadd("py-k3-" + str(i), i)
            p.execute()


def query():
    s = time.time()
    # for i in range(0,1000000):
    res = r.scan_iter("*_intercept_0_2017*", 10)
    for i in res:
        # print(i)
        pass

    e = time.time()
    print('---', (e - s))


def keys():
    s = time.time()

    res = r.keys("*")
    for i in res:
        print(i)
    print(len(res))

    e = time.time()
    print('---', (e - s))


if __name__ == '__main__':
    main()
    # query()
    # keys()
    # r.delete('*_intercept_0_2018*')
