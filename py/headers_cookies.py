#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/7/30

import os
import random
import sqlite3
import browser_cookie3

header_str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


def get_headers():
    headers = {
        'user-agent': header_str
    }
    return headers


def get_cookies_from_chrome():
    host_url = 'acm.hdu.edu.cn'
    # cookies_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    # sql_query = "select host_key, name, encrypted_value ,value from cookies WHERE host_key='%s'" % host_url
    # with sqlite3.connect(cookies_path) as con:
    #     cu = con.cursor()
    # cu.execute(sql_query)
    # cookies_sql = {name: win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value, value in cu.execute(sql_query).fetchall()}

    return browser_cookie3.chrome(domain_name=host_url)


print(get_cookie_from_chrome())