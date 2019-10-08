# coding:utf-8
#@Time : 2019/09/02  08:41
#author : Around
from django.urls import path

from cartapp import views
app_name='cartapp'
urlpatterns=[
    path('show_cart',views.show_cart,name='show_cart'),
    path('show_indent',views.show_indent,name='show_indent'),
    path('show_indent_ok',views.show_indent_ok,name='show_indent_ok'),
    path("add_to_cart",views.add_to_cart,name='add_to_cart'),
    path("totalprice",views.totalprice,name='totalprice'),
    path("del_cart_book",views.del_cart_book,name='del_cart_book'),
    path("indent_logic",views.indent_logic,name='indent_logic'),
    path("validate_addr",views.validate_addr,name='validate_addr'),
]