# mod = getattr(__import__('app',globals(),locals(),['handlers']),'handlers')
# for n in dir(mod):
#     print(n)

import inspect
def foo(a, *, b:int, **kwargs):
    pass
sig = inspect.signature(foo).parameters
print(sig)
for name,param in sig.items():
    print(name)
    print(param.kind)
