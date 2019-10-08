
# coding:utf-8
#@Time : 2019/09/03  09:26
#author : Around

import os
from django.core.mail import send_mail,EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'middle_project.settings'

if __name__ == '__main__':
    # send_mail()
    while 1:
        html_content = "<html><a href='http://www.baidu.com'>我是你的爸爸呀！</a></html>"
        msg = EmailMultiAlternatives(subject='我是你的爸爸',body=html_content,from_email='ijioijikk@163.com',to=['1427929372@qq.com'])
        msg.attach_alternative(html_content,"text/html")
        msg.send()


















