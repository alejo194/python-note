#### 1.python读csv文件
```bash
##用reader读取csv文件
with open('test.csv','r') as csvFile:
    reader = csv.reader(csvFile)
    for line in reader:
        print(line)
```
