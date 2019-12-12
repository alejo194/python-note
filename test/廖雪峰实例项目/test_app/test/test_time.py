import time
time1 = time.time()
print(time1)

class Test:
    def __new__(cls):
        print('__new___')
        return '1'

    def __init__(self):
        print('__init__')
        return 'test'


t=Test()
print(t)
