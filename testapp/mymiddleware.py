# coding:utf-8
#@Time : 2019/09/04  17:46
#author : Around

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)

    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        # 判断登录状态
        path_ban = ['/cartapp/show_indent','/cartapp/show_indent_ok']
        if request.path == path_ban[0]:
            request.session['re_path'] = request.path
        elif request.path == path_ban[1]:
            request.session['re_path'] = request.path
        if 'login' not in request.path and request.path in path_ban:
            if request.session.get('email'):
                print('ok')
            else:
                return redirect('testapp:login')
        print( "request:", request )


    # view执行之后，响应之前执行
    def process_response(self, request, response):
        print( "response:", request, response )
        return response  # 必须返回response