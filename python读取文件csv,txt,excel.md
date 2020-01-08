#### 1.python读写csv文件
```bash
import csv

with open('test.csv','w') as csvFile:
    writer = csv.writer(csvFile)
    #先写columns_name
    writer.writerow(['index','a_name','b_name'])
    #写入多行用writerows
    writer.writerows([[1,2,3],[0,1,2],[4,5,6]])

##用reader读取csv文件
with open('test.csv','r') as csvFile:
    reader = csv.reader(csvFile)
    for line in reader:
        print(line)
```
+ 一定要注意，csv文件在写入时，字段和字段之间是用逗号"",""分割的，如果稍不注意，就会出现串行的情况

#### 2.python读写excel文件
```bash
```

#### 3.python读写txt文件
```bash
```
