#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/10

from py.submit_code import *

code = """#include <iostream>
            using namespace std;
            int main()
            {
            int a, b;
            int sum = 0;
            while (cin >> a>> b)
            {
            cout << a + b << endl;
            }
            return 0;
            }"""
# e = HduSubmitter()
# e.login(username='940657598', password='guokun921')
# e.submit(language='2', problem='1000', code=code)
# e.get_result()
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }

submit_url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
data = {
            'check': 1,
            'problemid': '1000',
            'language': '3',
            'usercode': code
        }
requests.post(submit_url, data=data, headers=headers)
url = 'http://acm.hdu.edu.cn/status.php?user=940657598'
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
'''


class Test:

    def __init__(self):
        self.login_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'  # 这是hdu的登陆界面地址
        self.login_data = {"username": "940657598",
                           "userpass": "guokun921",
                           "login": "Sign In"
                           }
        self.question_url_pre = "http://acm.hdu.edu.cn/showproblem.php?pid="
        self.problem_url = ""
        self.problem_id = ""
        self.coding = ""
        self.problem_name = ""
        self.source = ""
        self.submit_data = {"check": "1",
                            "problemid": "1000",
                            "language": "2",
                            "usercode": code,
                            }
        self.submit_url = "http://acm.hdu.edu.cn/submit.php?action=submit"
        self.login_data = urllib.parse.urlencode(self.login_data).encode('utf-8')
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        self.pattern_title = 'lang="en-US">(.)*?</div>'

    def login(self):
        requ = urllib.request.Request(url=self.login_url, data=self.login_data, headers=self.headers)
        cjar = http.cookiejar.CookieJar()  # 创建一个CookieJar对象
        # 使用HTTPCookieProcessor创建一个cookie处理器 并且用它当参数构建opener对象
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
        # 把opener安装为全局
        urllib.request.install_opener(opener)
        file = opener.open(requ)
    # with open("test.html" , "wb") as fhandler:
    #	fhandler.write(file.read())

    def submit(self):
        # self.submit_data["problemid"] = str(page)
        try:
            self.submit_data["usercode"] = self.coding
        except Exception as E:
            print("错误发生在这里 快来看我  line 81 " + str(E))
        self.submit_data = urllib.parse.urlencode(self.submit_data).encode('utf-8')
        # self.headers["Referer"] = "http://poj.org/submit?problem_id=" + str(page)
        requ = urllib.request.Request(url=self.submit_url, data=self.submit_data, headers=self.headers)
        try:
            html = urllib.request.urlopen(requ, timeout=15)
        except Exception as E:
            print(E)
    # with open("file.html" , "wb") as fhandler:
    #	fhandler.write(html.read())
    # print("submit模块")
    #

t =Test()
t.login()
t.submit()