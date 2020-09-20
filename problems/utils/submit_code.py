#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/15

import sys
from random import randint

import requests
import time
import base64
from urllib.request import quote, unquote
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from problems.models import SubmitAccount


class SourceList():
    HDU = 'HDU'
    POJ = 'POJ'


class HDUSubmit(object):

    log_url = 'http://acm.hdu.edu.cn/userloginex.php?action=login'
    submit_url = 'http://acm.hdu.edu.cn/submit.php?action=submit'
    status_url = 'http://acm.hdu.edu.cn/status.php?'
    language_map = {
        "C#": 6,
        "Java": 5,
        "Pascal": 4,
        "C": 3,
        "Cpp": 2,
        "GCC": 1,
        "G++": 0
    }

    def __init__(self, user_id, password):
        '''

        :param user_id: 提交代码的机器人ID
        :param password: 提交代码的机器人密码密码
        '''
        self.id = user_id
        self.password = password
        self.session = requests.session()
        self.session.headers.update({
            'Origin': 'http://acm.hdu.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://acm.hdu.edu.cn',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',

        })
        self.cookie_jar = requests.cookies.RequestsCookieJar()

    def login(self):
        # if not self.is_login_in():
        params = {
            "username": self.id,
            "userpass": self.password,
            "login": "Sign In"
        }
        r = self.session.request(
            'POST',
            self.log_url,
            data=params,
            cookies=self.cookie_jar)

        print('log status_code:', r.status_code)
        return r

    def is_login_in(self):
        r = self.session.get("http://acm.hdu.edu.cn/control_panel.php")
        return r.status_code == 200

    def submit(self, pid, code, language='Cpp'):
        '''
        提交代码
        :param pid:题目ID
        :param code: 代码
        :param language:选择的语言
        :return: run_id
        '''
        self.login()
        code = quote(code)
        code = base64.b64encode(code.encode())
        code = str(code, encoding="utf8")  # 将代码编码
        params = {
            'check': 0,
            'problemid': pid,
            'language': self.language_map[language],
            '_usercode': code
        }
        r = self.session.request(
            'POST',
            self.submit_url,
            data=params,
            cookies=self.cookie_jar)

        print("submit status_code", r.status_code)

        if r.status_code == 200:
            print('submit success')
            time.sleep(0.1)
            return self.get_run_id()

        else:
            print('submit failed')
            return 'submit failed'

    def get_run_id(self):
        url = 'http://acm.hdu.edu.cn/status.php?user=' + self.id
        print(url)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        try:
            run_id = int(soup.findAll('table')[-2].findAll("tr")[1].td.string)
            return run_id
        except Exception as e:
            print(e)
            self.id = 1000
            return 1000


def hdu_get_result(run_id, hdu_id):
    '''
    爬取题目的提交结果
    :param username: acm网站的用户
    :param run_id: 题目对应的run_id
    :param hdu_id: hdu用户提交ID
    :return: 结果
    '''
    if isinstance(run_id, int):
        url = 'http://acm.hdu.edu.cn/status.php?user=' + hdu_id
        time.sleep(0.5)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        x = soup.find(text=run_id).parent.next_sibling
        print(x)
        while x.next_sibling.text in ['Queuing', 'Compiling', 'Running']:
            time.sleep(1)
            html = urlopen(url)
            soup = BeautifulSoup(html, 'lxml')
            x = soup.find(text=run_id).parent.next_sibling
        result = {
            'submit_time': x.text,
            'result': x.next_sibling.text,
            'problem_id': x.next_sibling.next_sibling.text,
            'time': int(re.sub(r"\D", "", x.next_sibling.next_sibling.next_sibling.text)),
            'memory': int(re.sub(r"\D", "", x.next_sibling.next_sibling.next_sibling.next_sibling.text)),
            'code_length': int(re.sub(r"\D", "", x.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text)),
            'lang': x.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text,
        }
        return result
    else:
        return run_id #此时的run_id编程了’submit_faild‘


def get_account(source):
    '''
    根据来源随机获得账号密码，
    里边的5是根据账号的数量写的
    :param source: 来源
    :return: 账号，密码
    '''
    index = randint(0, 1)
    robot = SubmitAccount.objects.filter(source=source)[index]
    return robot.account_id, robot.account_password


def main_function(source, code, language, problem_id):
    '''

    :param source:题目来源
    :param code: 题目代码
    :param language: 提交语言
    :param problem_id: 题目ID
    :return: 返回查找结果
    '''
    account_id, account_password = get_account(source)
    # account_id = '940657598'
    # account_password = 'guokun921'
    if source == SourceList.HDU:
        robot = HDUSubmit(account_id, account_password)
        run_id = robot.submit(problem_id, code, language)
        return hdu_get_result(run_id=run_id, hdu_id=account_id)
    elif source == SourceList.POJ:
        pass
'''
    def status(self, pid):  # 返回最近一次提交
        params = {
            'pid': pid,
            'user': self.id
        }
        r = self.session.get(self.status_url, params=params)
        soup = BeautifulSoup(r.text, 'lxml')
        trs = soup.find('div', {'id': 'fixed_table'})('tr')
        model = [td.string for td in trs[0]('td')]
        data = [td.string for td in trs[1]('td')]
        pat = ['{:^%d}' % (max(len(model[i]), len(data[i])))
               for i in range(len(data))]
        for i in range(len(model)):
            print(pat[i].format(model[i]), end=' ')
        print()
        for i in range(len(data)):
            print(pat[i].format(data[i]), end=' ')
        return r

    def status_by_runid(self, rid):  # 返回最近一次提交
        params = {
            'first': rid,

        }
        r = self.session.get(self.status_url, params=params)
        soup = BeautifulSoup(r.text, 'lxml')
        trs = soup.find('div', {'id': 'fixed_table'})('tr')
        model = [td.string for td in trs[0]('td')]
        data = [td.string for td in trs[1]('td')]
        pat = ['{:^%d}' % (max(len(model[i]), len(data[i])))
               for i in range(len(data))]
        for i in range(len(model)):
            print(pat[i].format(model[i]), end=' ')
        print()
        for i in range(len(data)):
            print(pat[i].format(data[i]), end=' ')
        return r


'''
# def read_code(filename):
#     code = None
#     with open(filename, 'rb') as f:
#         code = f.read()
#     return code
'''


def main(lan='Cpp', argv=None):
    print("请输入id和密码:")
    id = "1139571193"
    ps = "wzl123"
    fname = "1000.cpp"
    pnumber = 1067

    # code = read_code(fname)
    hdu = HDUSubmit(id, ps)
    hdu.login()
    hdu.submit(pnumber, code, lan)
    print()
    hdu.status_by_runid(33926234)  # 根据rid查找运行结果


if __name__ == '__main__':
    main()
'''
