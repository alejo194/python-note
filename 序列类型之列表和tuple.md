#### 列表
```bash
容器类型：
    任意对象的有序集合，通过索引访问其中的元素，可变对象，
    异构，任意嵌套
    
支持在原处修改：
    修改指定的索引元素，修改指定的分片，删除语句，内置方法

l1 + l2: 合并两个列表，返回一个新的列表；不会改变原列表；
l1 * N: 把l1重复N次，返回一个新列表；

in: 成员关系判断字符，用法 obj in container
no in: obj not in container

列表解析：[表达式]

列表复制方式：
    l1 = [1,2,3,4]
    l2 = l1  ###指向l1地址
    
    import copy
    l2 = copy.deepcopy(l1)  ###创建一个新列表
    
    l2 = l1[:]  ###创建一个新列表
```
##### 列表的常用操作
```bash
append()
sorte()
reverse()
clear()
count()
extend(iterable)
index()
pop()
remove()
深浅拷贝，随机数
```
#### tuple
