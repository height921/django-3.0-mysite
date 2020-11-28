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
        "4": 6,# c#
        "2": 5, #java
        "5": 4, #gcc
        "3": 3,# c
        "0": 2, # c++
        "1": 0 # g++
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
            self.run_id = self.get_run_id()

        else:
            print('submit failed')
            self.run_id = 'submit failed'

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

    def get_result(self):
        '''
        爬取题目的提交结果
        :param username: acm网站的用户
        :param run_id: 题目对应的run_id
        :param hdu_id: hdu用户提交ID
        :return: 结果
        '''
        if isinstance(self.run_id, int):
            url = 'http://acm.hdu.edu.cn/status.php?user=' + self.id
            time.sleep(0.5)
            html = urlopen(url)
            soup = BeautifulSoup(html, 'lxml')
            x = soup.find(text=self.run_id).parent.next_sibling
            while x.next_sibling.text in ['Queuing', 'Compiling', 'Running']:
                time.sleep(1)
                html = urlopen(url)
                soup = BeautifulSoup(html, 'lxml')
                x = soup.find(text=self.run_id).parent.next_sibling
            result = {
                'submit_time': x.text,
                'result': x.next_sibling.text,
                'problem_id': x.next_sibling.next_sibling.text,
                'time': int(re.sub(r"\D", "", x.next_sibling.next_sibling.next_sibling.text)),
                'memory': int(re.sub(r"\D", "", x.next_sibling.next_sibling.next_sibling.next_sibling.text)),
                'code_length': int(
                    re.sub(r"\D", "", x.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text)),
                'lang': x.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text,
            }
            return result
        else:
            return self.run_id  # 此时的run_id变成了’submit_failed‘


class POJSubmit():
    main_url = 'http://poj.org'
    language_map = {
        "3": 5, #c
        "0": 4, #c++
        "5": 3,# pascal
        "2": 2, # java
        "4": 1, #gcc
        "1": 0 # g++
    }
    def __init__(self, user_id, password):
        self.session = requests.session()
        self.user_id = user_id
        self.password = password
        self.is_login = False

    def login(self):

        if self.is_login:
            print('You Have Loged in!')

            return False

        login_data = {
            'user_id1': self.user_id,
            'password1': self.password,
            'B1': 'login',
            'url': '/'
        }
        r = self.session.post(POJSubmit.main_url + '/login', data=login_data)
        r = self.session.get(POJSubmit.main_url + '/send?to=' + self.user_id)

        s = re.search('Error', r.text)
        self.is_login = s is None
        if self.is_login:
            print('Login OK!')

        else:
            print('Login Failed!')
        return s is None

    def submit(self, code, prob_id, lang):

        if not self.is_login:
            print('Please Login First!')
            self.login()

        self.prob_id = prob_id
        self.lang = self.language_map[lang]
        code = base64.b64encode(code.encode())
        code = str(code, encoding="utf8")  # 将代码编码
        submit_data = {
            'problem_id': prob_id,
            'language': self.lang,
            'source': code,
            'submit': 'Submit',
            'encoded': 1
        }
        r = self.session.post(POJSubmit.main_url + '/submit', data=submit_data)

        if r.status_code != 200:
            print('Submit Failed!')

            return False
        else:
            print("Submitted!")

    def get_result(self):
        status = POJSubmit.main_url + '/status?problem_id=%s&user_id=%s&result=&language=%d' \
            % (self.prob_id, self.user_id, self.lang)
        print('url',self.prob_id,self.user_id,self.lang)
        status_id = '0'
        results = [
            'Accepted',
            'Presentation Error',
            'Time Limit Exceeded',
            'Memory Limit Exceeded',
            'Wrong Answer',
            'Runtime Error',
            'Output Limit Exceeded',
            'Compile Error',
            'System Error',
            'Validator Error',
        ]
        result = {}
        while True:
            found = False
            res = ''
            r = self.session.get(status)
            print('Waiting for status...')

            soup = BeautifulSoup(r.text, "lxml")
            tbs = soup.find_all(self.__stat_tab)[0]
            # tbs = soup.find_all()[0]
            detail = ''
            for i, tr in enumerate(tbs.find_all('tr')):
                print(tr.td.contents[0])
                if status_id == '0' and i == 1:
                    status_id = tr.td.contents[0]
                if status_id == tr.td.contents[0]:
                    res = tr.find_all('td')[3].font.contents[0]
                    detail = tr
            print("status_id", status_id)
            print("ret", res)
            for ret in results:
                if ret == res:
                    result['Run ID'] = detail.find_all('td')[0].contents[0]
                    result['User'] = detail.find_all('td')[1].contents[0].text
                    result['Problem'] = detail.find_all(
                        'td')[2].contents[0].text
                    result['code_length'] = re.sub(r"\D", "",detail.find_all('td')[7].contents[0])
                    result['submit_time'] = re.sub(r"\D", "",detail.find_all('td')[8].contents[0])
                    result['lang'] = detail.find_all('td')[6].contents[0].text
                    result['result'] = res
                    if len(detail.find_all('td')[4].contents) > 0:
                        result['memory'] = re.sub(r"\D", "",detail.find_all('td')[4].contents[0])
                    else:
                        result['memory'] = ''
                    if len(detail.find_all('td')[5].contents) > 0:
                        result['time'] = re.sub(r"\D", "",detail.find_all('td')[5].contents[0])
                    else:
                        result['time'] = ''
                    found = True
                    print('Have Got the Result!')

                    break
            if found:
                break
        print("result",result)
        return result

    def __stat_tab(self, tag):
        '''
        ignore tables which is no the submission table
        '''
        return tag.has_attr('class') and tag['class'] == ['a']


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
    if source == SourceList.HDU:
        robot = HDUSubmit(account_id, account_password)
        robot.submit(problem_id, code, language)
        return robot.get_result()
    elif source == SourceList.POJ:
        robot = POJSubmit(account_id, account_password)
        print("lang",language)
        robot.submit(prob_id=problem_id, code=code,lang=language)
        return robot.get_result()