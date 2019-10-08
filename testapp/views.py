import json
import random
import string
from _sha1 import sha1

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from cartapp.car import Cart
from testapp.captcha.image import ImageCaptcha
from testapp.models import Category, TBook, User, TShoppingCart


def index(request):
    status = request.session.get( 'status' )# 获取是否有登录状态
    email_cookie = request.COOKIES.get('email')
    email_pwd = request.COOKIES.get('pwd')

    request.session['re_path'] = request.path
    name = request.session.get('email')
    cate_one = Category.objects.filter( pid=0 )
    cate_two = Category.objects.filter( pid__gt=0 )
    new_book = TBook.objects.all().order_by('shelves_date')[:8]
    editor_recommend_book = TBook.objects.order_by('-rel_price')[:12]
    new_hot_book = TBook.objects.order_by('-shelves_date','-sales')[:5]
    new_hot_book1 = TBook.objects.order_by( '-shelves_date', '-sales' )[:10]
    return render( request, 'index.html', {'cate_one': cate_one,
                                           'cate_two': cate_two,
                                           'new_book':new_book,
                                           'editor_book':editor_recommend_book,
                                           'new_hot_book':new_hot_book,
                                           'new_hot_book1':new_hot_book1,
                                           'status':status,
                                           'name':name} ,
                   )
def book_details(request):
    status = request.session.get('status')
    name = request.session.get( 'email' )
    book_id = request.GET.get( 'book_id' )#书的id
    if TBook.objects.filter(id=book_id):
        request.session['re_path'] = request.path
        request.session['id'] = book_id
        res = TBook.objects.filter(id=book_id)
        cate_id = res[0].cate_id #通过书的id找到该条数据对应的类别id
        cate_son = Category.objects.filter( id=cate_id )#通过找到的类别id找到子类
        cate_parent = Category.objects.filter( id=cate_son[0].pid )#通过子类找到父类
        return render(request,'Book details.html',{'res':res, 'cate_son':cate_son,
                                               'cate_parent':cate_parent,'status':status,
                                               'name':name})
    else:
        book_id = request.session.get('id')
        return redirect("/testapp/book_details/?book_id="+book_id)
def book_list(request):
    status = request.session.get( 'status' )
    name = request.session.get( 'email' )

    cate_one = Category.objects.filter( pid = 0 )
    cate_two = Category.objects.filter( pid__gt=0 )
    id = request.GET.get('id')
    request.session['re_path'] = request.path
    request.session['id'] = id
    pageid = request.GET.get('page_id')
    slice_page = '0:6'
    if pageid is None:
        pageid = 1
    if Category.objects.filter(id=id):
        cate = Category.objects.filter(id=id)  #先获取该id对应的信息
        cate_parent = Category.objects.filter( id=cate[0].pid )# 获取父类
        status1 = 0
        if cate_parent:# 如果有值，则说明这是二级分类
            relate_book = TBook.objects.filter( cate_id=id )
            paginator = Paginator(relate_book,per_page=3)
            page = paginator.page(pageid)
            status1 = 2
        else:# 否则，你点击的是一级类别
            cate_parent = Category.objects.filter(id = id)
            # 通过大类id获取小类的pid
            #获取的是大类id对应的所有小类
            second_id = Category.objects.filter(pid = id)
            # 将小类的pid放到一个列表
            list1 = []
            for i in second_id:
                list1.append(i.id)
            # 通过二级pid与书籍的cate_id拼接
            relate_book = TBook.objects.filter( cate_id__in=list1 )
            paginator = Paginator( relate_book, per_page=3 )
            page = paginator.page( pageid )

            if page.number > 5:
                slice_page = str(page.number-4) + ":" + str(page.number+3)
            status1 = 1
        return render(request,'booklist.html',{'cate_one':cate_one,
                                               'cate_two':cate_two,
                                               'relate_book':relate_book,
                                               'cate_son':cate,
                                               'cate_parent':cate_parent,
                                               'page':page,
                                               'id':id,
                                               'status1':status1,
                                               'slice_page':slice_page,
                                               'status': status,
                                               'name':name,})
    else:
        return redirect('/testapp/book_list/'+"?id=1")

def relate_book_def(relate_book):
    if isinstance(relate_book,TBook):
        return {'id':relate_book.id,
                'book_name':relate_book.book_name,
                'comment':relate_book.comment,
                'author':relate_book.author,
                'publish_time':relate_book.publish_time,
                'publisher':relate_book.publisher,
                'author_intro':relate_book.author_intro,
                'rel_price':relate_book.rel_price,
                'original_cost':relate_book.original_cost,
                }
def book_order_by_price(request):
    id = request.GET.get('id') # 获取类别
    relate_book = TBook.objects.filter(cate_id = id).order_by('-rel_price')
    return JsonResponse(list(relate_book),safe=False,json_dumps_params={'default':relate_book_def})
    # return render(request,'booklist.html',{'relate_book':relate_book})
def create_captcha(request):
    image = ImageCaptcha()
    code_list = random.sample( string.ascii_letters + string.digits, 4 )
    random_str = ''.join( code_list )
    request.session['code'] = random_str
    # 生成验证码图片
    data = image.generate( random_str )
    return HttpResponse( data, 'image/png' )
def captcha_is_right(request):
    captcha_val = request.POST.get('captcha_val')
    session_code_val = request.session.get('code')
    print(session_code_val)
    if captcha_val.lower() == session_code_val.lower():
        return HttpResponse('1')
    else:
        return HttpResponse('0')
def regist(request):
    return render(request,'register.html')
def show_regist_ok(request):
    email = request.session.get('email')
    request.session['status'] = '1'
    path1 = request.session.get('path1')
    re_path = request.session.get( 're_path' )
    re_id = request.session.get( 'id' )
    path = ''
    if path == '':
        path = "/testapp/index/"
    if path1 == "/cartapp/show_cart":
        path = "/cartapp/show_indent"
    if re_path == "/testapp/book_list/":
        path = re_path + "?id=" + re_id
    if re_path == "/testapp/book_details/":
        path = re_path + "?book_id=" + re_id
    if  re_path == "/testapp/index/":
        path = re_path
    return render(request,'register ok.html',{'email':email,'path':path})
def regist_logic(request):
    useremail = request.POST.get('txt_username')
    password = request.POST.get('txt_password')
    #加密
    s1 = sha1()
    s1.update( password.encode( 'utf8' ) )
    password1 = s1.hexdigest()
    s = '123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+'
    pwd_prefix = random.sample(s,5)
    pwd_prefix = ''.join(pwd_prefix)
    res = User.objects.create(user_email=useremail,password=pwd_prefix+password1,user_prefix=pwd_prefix)
    if res:
        request.session['email'] = useremail
        request.session['pwd'] = pwd_prefix+ password1
        request.session['status'] = '1'
        login_logic(request)
        return redirect('testapp:show_regist_ok')
    else:
        return render(request,'register.html')
def name_is_exist(request):
    value = request.POST.get('value')#获取邮箱或者手机号
    res = User.objects.filter(user_email=value)#数据库中查找有没有相同的
    if res:# 如果有，那就不能注册，返回0
        return HttpResponse('0')
    else:#如果没有，那就可以注册，返回1
        return HttpResponse('1')
def login(request):
    email = request.COOKIES.get('email')
    pwd = request.COOKIES.get('pwd')
    auto_login = request.COOKIES.get('auto_login')
    res = User.objects.filter(user_email=email,password=pwd)
    if res and auto_login=='true':
        return render( request, 'login.html' ,{'email':email,'pwd':pwd})
    else:
        return render(request,'login.html',{'email':'','pwd':''})
def login_logic(request):# 这里是为了，在index界面直接进入订单界面。提前获取数据库中的值，保存到session
    status = request.session.get('status')
    name = request.session.get('email')
    if status:
        # 获取未登录时的session中的图书，加入购物车
        cart = request.session.get( 'cart' )
        user_id = User.objects.filter( user_email=name )  # 获取当前登录的用户
        if cart:
            for i in cart.cart_items:# 将未登录前的数据加入购物车数据库
                re1 = TShoppingCart.objects.filter(bookid=i.book.id,userid=user_id[0].id)# 判断数据库中是否有这本书，如果有的话，只需修改书籍数量
                if re1:
                    re1[0].count = i.count
                    re1[0].save()
                else:#数据库中没有这本书，那么就将书信息添加进去
                    r = TShoppingCart.objects.create( count=i.count, userid=user_id[0].id, bookid=i.book.id )
            del request.session['cart']
        res = TShoppingCart.objects.filter( userid=user_id[0].id )  # 获取当前登录的用户,找到对应的购物车信息
        bookid_list = []  # 通过用户id，查询该用户添加了哪些书籍，将书籍id保存在列表中
        for j in res:
            bookid_list.append( j.bookid )
        re2 = TBook.objects.filter( id__in=bookid_list )  # 通过查出的书籍id获取这些书籍的信息
        cart_new = Cart()
        for k in range( len( re2 ) ):
            count1 = TShoppingCart.objects.filter( bookid=re2[k].id )[0].count
            cart_new.add_car( re2[k], count1 )
            request.session['cart_new'] = cart_new
def login_right(request):
    name = request.POST.get( 'name' )  # 获得输入框的账号
    pwd = request.POST.get( 'pwd' )  # 获取输入框中的密码
    pwd_cookie = request.COOKIES.get( 'pwd' )  # 获得cookie中的密码,前面有'zw'前缀
    auto_login = request.POST.get( 'auto_login' )  # 获取登录状态
    re_path = request.session.get('re_path')
    print(re_path)
    re_id = request.session.get('id')
    path=''
    if re_path == "/testapp/book_list/":
        path = re_path+"?id="+re_id
    if re_path == "/testapp/book_details/":
        path = re_path+"?book_id="+re_id
    if re_path == "/testapp/index/":
        path = re_path
    if re_path == "/cartapp/show_cart":
        path = re_path
    if re_path == "/cartapp/show_indent":
        path = re_path
    if re_path == "/cartapp/show_indent_ok":
        path = "/cartapp/show_indent"
    s1 = sha1()  # 加密
    s1.update( pwd.encode( 'utf-8' ) )
    pwd1 = s1.hexdigest()
    if pwd == pwd_cookie:  # 判断框中的密码和cookie中的是否一致，一致则使用pwd
        res = User.objects.filter( user_email=name, password=pwd ) # 判断数据库中是否正确
        if res:# 如果账号密码和数据库中的匹配，则保存账号，密码，登录状态到session
            request.session['email'] = name
            request.session['pwd'] = pwd
            request.session['status'] = '1'
            login_logic(request)
            response = HttpResponse( path )
            if auto_login == 'true':#如果勾选了7天免登陆按钮，则设置免登录状态，账号，密码到cookie
                response.set_cookie( 'auto_login', auto_login, max_age=7 * 24 * 3600 )
                response.set_cookie( 'email', name, max_age=7 * 24 * 3600 )
                response.set_cookie( 'pwd', pwd, max_age=7 * 24 * 3600 )
            else:
                response.set_cookie( 'auto_login', auto_login, max_age=0 )
                response.set_cookie( 'email', name, max_age=0 )
                response.set_cookie( 'pwd', pwd, max_age=0 )
            return response
        else:
            return HttpResponse( '0' )
    else:  # 如果不一致，则使用加密后的密码
        res_prefix = User.objects.filter(user_email=name)
        prefix = res_prefix[0].user_prefix
        res = User.objects.filter( user_email=name, password=prefix+pwd1 )
        if res:
            request.session['email'] = name
            request.session['pwd'] = res[0].user_prefix+pwd1
            request.session['status'] = '1'
            login_logic( request )
            response = HttpResponse( path )
            if auto_login == 'true':
                response.set_cookie( 'auto_login', auto_login, max_age=7 * 24 * 3600 )
                response.set_cookie( 'email', name, max_age=7 * 24 * 3600 )
                response.set_cookie( 'pwd', res[0].user_prefix+pwd1, max_age=7 * 24 * 3600 )
            else:
                response.set_cookie( 'auto_login', auto_login, max_age=0 )
                response.set_cookie( 'email', name, max_age=0 )
                response.set_cookie( 'pwd', pwd, max_age=0 )
            return response
        else:
            return HttpResponse( '0' )
def logout(request):
    re_path = request.session.get( 're_path' )
    re_id = request.session.get( 'id' )
    path = ''
    if re_path == "/testapp/book_list/":
        path = re_path + "?id=" + re_id
    if re_path == "/testapp/book_details/":
        path = re_path + "?book_id=" + re_id
    if re_path == "/testapp/index/":
        path = re_path
    if re_path == "/cartapp/show_cart":
        path = re_path
    if re_path == "/cartapp/show_indent":
        path = "/testapp/index"
    if re_path == "/cartapp/show_indent_ok":
        path = "/testapp/index"
    request.session.flush()
    return redirect( path )



