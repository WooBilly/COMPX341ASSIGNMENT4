import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
cache.delete('myList')
isEmpty = 0
lis = []

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/isPrime/<int:number>')
def isPrime(number):
    num = number
    prime = 2
    if num == prime:
        global lis
        if num not in lis:
            lis.append(num)
            cache.append('myList','{} '.format(num))
        global isEmpty
        isEmpty = 1
        return '{} is prime.'.format(num)
    elif num < prime:
        return '{} is not prime.'.format(num)
    elif num == 2147483647:
        if num not in lis:
            lis.append(num)
            cache.append('myList','{} '.format(num))
        return '{} is prime.'.format(num)
    elif num > prime:
        for i in range(2,num):
            if(num % i) == 0:
                return '{} is not prime.'.format(num)
                break
        if num not in lis:
            lis.append(num)
            cache.append('myList','{} '.format(num))
        return '{} is prime.'.format(num)

@app.route('/primesStored')
def primesStored():
    if isEmpty == 1:
        return cache.get('myList')
    else:
        return "There is no list"

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello from Docker! I have been seen {} times.\n'.format(count)
