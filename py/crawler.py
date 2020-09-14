#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/9/10

# 交给凌歆鹏了
'''
爬杭电，网站搜来的代码
'''
import requests
from bs4 import BeautifulSoup
import time
import random
import re
from requests.exceptions import RequestException


prbm_id = []
prbm_name = []
prbm_ac = []
prbm_sub = []


def get_html(url):   # 获取html
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=5, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        random_time = random.randint(1, 3)
        time.sleep(random_time)    # 应对反爬虫，随机休眠1至3秒
        return r.text
    except RequestException as e:  # 异常输出
        print(e)
        return ""


def get_hdu():
    count = 0
    for i in range(1, 59):
        url = "http://acm.hdu.edu.cn/listproblem.php?vol=" + str(i)
        # print(url)
        html = get_html(url)
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        cnt = 1
        for it in soup.find_all("script"):
            if cnt == 5:
                # print(it.get_text())
                str1 = it.string
                list_pro = re.split("p\(|\);", str1)   # 去除 p(); 分割
                # print(list_pro)
                for its in list_pro:
                    if its != "":
                        # print(its)
                        temp = re.split(',', its)
                        len1 = len(temp)
                        prbm_id.append(temp[1])
                        prbm_name.append(temp[3])
                        prbm_ac.append(temp[len1-2])
                        prbm_sub.append(temp[len1-1])
            cnt = cnt + 1
        count = count + 1
        print('\r当前进度：{:.2f}%'.format(count * 100 / 55, end=''))  # 进度条


def main():
    get_hdu()
    root = "D:\\学习使我快乐\\Py_study\\爬杭电\\hdu题目数据爬取2.txt"
    len1 = len(prbm_id)
    for i in range(0, len1):
        with open(root, 'a', encoding='utf-8') as f:  # 存储个人网址
            f.write("hdu"+prbm_id[i] + "," + prbm_name[i] + "," + prbm_ac[i] + "," + prbm_sub[i] + '\n')
        # print(prbm_id[i])


if __name__ == '__main__':
    main()