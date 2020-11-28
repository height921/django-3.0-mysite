#!python
# -*- encoding:utf-8 -*-
# Created by admin at 2020/11/27


def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]  # python3