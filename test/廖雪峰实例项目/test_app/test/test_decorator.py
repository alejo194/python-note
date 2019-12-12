import functools
def test(pat):
    def logger(fn):
        @functools.wraps(fn)  # 加上输出的就是fn的函数名
        def wrap(*args, **dicts):
            '''
            wrap
            :param args:
            :param dicts:
            :return: ret fun
            '''
            print(args, dicts)
            ret = fn(*args, **dicts)
            return ret
        return wrap
    print(pat)
    return logger

@test('111')
def add(x,y):
    '''
    add
    :param x:
    :param y:
    :return:
    '''
    print(add.__name__, add.__doc__) # 输出的是装饰器的函数名
    return x+y

## 带参数的,先执行带参数的，在执行函数的
'''
@test('111')   
def add(x,y):
    return x+y
'''
# test=test('111')(add) ##与上面的注释等价
# print(test(1,2))

@test('111')
def tt():
    '''
    tt
    :return:
    '''
    print(tt.__name__, tt.__doc__) # 输出的是装饰器的函数名
    return 'tt'

print(add(1,2), tt())


