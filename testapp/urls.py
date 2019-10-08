# coding:utf-8
#@Time : 2019/08/27  17:15
#author : Around
from django.urls import path

from testapp import views
app_name = 'testapp'
urlpatterns = [
    path('index/',views.index,name='index'),
    path('book_details/',views.book_details,name='book_details'),
    path('book_list/',views.book_list,name='book_list'),
    path('book_order_by_price/',views.book_order_by_price,name='book_order_by_price'),
    path('regist/',views.regist,name='regist'),
    path('regist_logic/',views.regist_logic,name='regist_logic'),
    path('name_is_exist/',views.name_is_exist,name='name_is_exist'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('login_logic/',views.login_logic,name='login_logic'),
    path('login_right/',views.login_right,name='login_right'),
    path('create_captcha/',views.create_captcha,name='create_captcha'),
    path('captcha_is_right/',views.captcha_is_right,name='captcha_is_right'),
    path('show_regist_ok/',views.show_regist_ok,name='show_regist_ok'),


]