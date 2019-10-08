import random
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from cartapp.car import Cart, Cart_items
from testapp.models import User, TShoppingCart, TBook, TAddress, DOrderiterm, TOrder

def show_cart(request):
    email = request.session.get('email')
    status = request.session.get('status')
    request.session['re_path'] = request.path
    request.session['path1'] = request.path
    re=(0,0)
    cart_total=None
    if status == '0' or status == None:
        cart = request.session.get( 'cart' )
        if cart:
            re = cart.sums()
            cart_total = cart.cart_items
        else:
            re = (0,0)
            cart_total = []
    if status=='1':
        cart = request.session.get( 'cart' )
        user_id = User.objects.filter( user_email=email )# 获取当前登录的用户
        if cart:
            for i in cart.cart_items:# 将未登录前的数据加入购物车数据库
                re1 = TShoppingCart.objects.filter(bookid=i.book.id)# 判断数据库中是否有这本书，如果有的话，只需修改书籍数量
                if re1:
                    re1[0].count = i.count
                    re1[0].save()
                else:#数据库中没有这本书，那么就将书信息添加进去
                    TShoppingCart.objects.create( count=i.count, userid=user_id[0].id, bookid=i.book.id )
            del request.session['cart']
        res = TShoppingCart.objects.filter(userid=user_id[0].id)# 获取当前登录的用户,找到对应的购物车信息
        bookid_list = []# 通过用户id，查询该用户添加了哪些书籍，将书籍id保存在列表中
        for j in res:
            bookid_list.append(j.bookid)
        re2 = TBook.objects.filter(id__in=bookid_list)# 通过查出的书籍id获取这些书籍的信息
        cart_new = Cart()
        total_sums = 0
        cha_sums = 0
        for k in range(len(re2)):
            count1 = TShoppingCart.objects.filter(bookid=re2[k].id)[0].count
            cart_new.add_car(re2[k],count1)
            request.session['cart_new'] = cart_new
            total_sums += count1*re2[k].rel_price
            cha_sums += count1*(re2[k].original_cost-re2[k].rel_price)
        cart_total = cart_new.cart_items
        re = (total_sums,cha_sums)
    # print(cart)#<cartapp.car.Cart object at 0x000001D091D844E0>
    # print(cart.cart_items)#[<cartapp.car.Cart_items object at 0x000001D091D84710>, <cartapp.car.Cart_items object at 0x000001D091D96160>]
    # print(len(cart.cart_items),'16hang')# 2 16hang
    # print(cart.cart_items[1].count)# 5
    # print(cart.cart_items[1].book.book_name)
    return render(request,'car.html',{'email':email,'status':status,
                                      'cart':cart_total,'re':re,'cart_len':len(cart_total)})
def show_indent(request):
    status = request.session.get('status')
    email = request.session.get('email')
    # if status == '1':
    cart = request.session.get( 'cart' )
    print(cart,'67hang')
    user_id = User.objects.filter( user_email=email )  # 获取当前登录的用户
    print(user_id,'69hang')
    if cart:
        for i in cart.cart_items:  # 将未登录前的数据加入购物车数据库
            re1 = TShoppingCart.objects.filter( bookid=i.book.id )  # 判断数据库中是否有这本书，如果有的话，只需修改书籍数量
            if re1:
                re1[0].count = i.count
                re1[0].save()
            else:  # 数据库中没有这本书，那么就将书信息添加进去
                TShoppingCart.objects.create( count=i.count, userid=user_id[0].id, bookid=i.book.id )
        del request.session['cart']
    address = TAddress.objects.filter(user_id=user_id[0].id)
    res = TShoppingCart.objects.filter( userid=user_id[0].id )  # 获取当前登录的用户,找到对应的购物车信息
    print(res,'81hang')
    bookid_list = []  # 通过用户id，查询该用户添加了哪些书籍，将书籍id保存在列表中
    for j in res:
        bookid_list.append( j.bookid )
    re2 = TBook.objects.filter( id__in=bookid_list )  # 通过查出的书籍id获取这些书籍的信息
    c = request.session.get('cart_new') # 从购物车进入登录，再进入注册，注册成功后保存购物车的信息到数据库，并取出，制成一个cart对象，保存于session
    total_sums = 0
    cha_sums = 0
    cart_new = Cart()
    for k in range( len( re2 ) ):
        count1 = TShoppingCart.objects.filter( bookid=re2[k].id )[0].count
        cart_new.add_car( re2[k], count1 )
        total_sums += count1 * re2[k].rel_price
        cha_sums += count1 * (re2[k].original_cost - re2[k].rel_price)
    cart_total = cart_new.cart_items
    print(cart_total,'96hang')
    request.session['cart_new'] = cart_new
    re = (total_sums, cha_sums,total_sums+cha_sums)
    if cart_total is None:
        cart_total = []
    return render(request,'indent.html',{'status':status,'name':email, 'cart':cart_total,'re':re,
                                         'address':address,'cart_len':len(cart_total)})
    # else:
    #     return redirect('testapp:login')
def show_indent_ok(request):
    name = request.session.get('email')
    status = request.session.get('status')
    order_id = request.GET.get('order_id')
    give_name = request.GET.get('give_name')
    items_sum  = request.GET.get('items_sum')
    total_price = request.GET.get('total_price')
    return render(request,'indent ok.html',{'name':name,'status':status,'order_id':order_id,'give_name':give_name,'items_sum':items_sum,'total_price':total_price})
def add_to_cart(request):
    book_id = request.GET.get('id')
    book_count = request.GET.get('book_count')
    cart = request.session.get( 'cart' )
    status = request.session.get('status')
    if status == '0' or status == None:
        if cart is None:
            cart = Cart()  # 新创键一个购物车
            cart.add_car(TBook.objects.filter(id=book_id)[0],int(book_count))
            request.session['cart'] = cart
        else:
            cart.add_car(TBook.objects.filter(id=book_id)[0],int(book_count))
            request.session['cart'] = cart
        return HttpResponse( 'success' )
    elif status == '1':
        user_name = request.GET.get( 'user_name' )
        user_id = User.objects.filter( user_email=user_name )[0].id
        res = TShoppingCart.objects.filter(userid=user_id,bookid=book_id)# 如果存在这本书，则只需修改count值即可
        if res:
            res[0].count += int(book_count)
            res[0].save()
        re = TShoppingCart.objects.create(count=int(book_count),userid=user_id,bookid=book_id)
        if re:
            return HttpResponse( 'success' )
        else:
            return HttpResponse('error')
def totalprice(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    count = int(count)
    status = request.session.get('status')
    if status == '0' or status==None:
        cart1 = request.session.get('cart')
        for i in cart1.cart_items:
            if int(id) == i.book.id:
                i.count = count
        request.session['cart'] = cart1
        re = cart1.sums()
        return JsonResponse({'total':re[0],'save_price':re[1]})
    elif status == '1':
        email = request.session.get('email')
        res = TShoppingCart.objects.get(bookid=id)
        res.count = count
        res.save()

        user_id = User.objects.filter( user_email=email )  # 获取当前登录的用户
        res = TShoppingCart.objects.filter( userid=user_id[0].id )  # 获取当前登录的用户,找到对应的购物车信息
        bookid_list = []  # 通过用户id，查询该用户添加了哪些书籍，将书籍id保存在列表中
        for j in res:
            bookid_list.append( j.bookid )
        re2 = TBook.objects.filter( id__in=bookid_list )  # 通过查出的书籍id获取这些书籍的信息
        total_sums = 0
        cha_sums = 0
        for k in range( len( re2 ) ):
            count1 = TShoppingCart.objects.filter( bookid=re2[k].id )[0].count
            total_sums += count1 * re2[k].rel_price
            cha_sums += count1 * (re2[k].original_cost - re2[k].rel_price)
        re = (total_sums, cha_sums)
        return JsonResponse({'total':re[0],'save_price':re[1]})
def del_cart_book(request):
    id = request.GET.get('id')
    status = request.session.get( 'status' )
    if status == '0' or status==None:
        cart2 = request.session.get('cart')
        for i in cart2.cart_items:
            if i.book.id == int(id):
                cart2.cart_items.remove( i )
                cart2.del_items.append( Cart_items( TBook.objects.filter( id=id ), i.count ) )
        request.session['cart'] = cart2
        re = cart2.sums()
        return JsonResponse({'total':re[0],'save_price':re[1]})
    elif status == '1':
        re = TShoppingCart.objects.filter(bookid=id)
        re.delete()

        email = request.session.get( 'email' )
        user_id = User.objects.filter( user_email=email )  # 获取当前登录的用户
        res = TShoppingCart.objects.filter( userid=user_id[0].id )  # 获取当前登录的用户,找到对应的购物车信息
        bookid_list = []  # 通过用户id，查询该用户添加了哪些书籍，将书籍id保存在列表中
        for j in res:
            bookid_list.append( j.bookid )
        re2 = TBook.objects.filter( id__in=bookid_list )  # 通过查出的书籍id获取这些书籍的信息
        total_sums = 0
        cha_sums = 0
        for k in range( len( re2 ) ):
            count1 = TShoppingCart.objects.filter( bookid=re2[k].id )[0].count
            total_sums += count1 * re2[k].rel_price
            cha_sums += count1 * (re2[k].original_cost - re2[k].rel_price)
        re = (total_sums, cha_sums)
        return JsonResponse( {'total': re[0], 'save_price': re[1]} )
def indent_logic(request):
    value = request.GET.get('value')
    if value == "--请选择--":
        return JsonResponse({'detail_address':'','name':'','zipcode':'','telphone':'','addr_phone':''})
    else:
        val = value.split('/')
        return JsonResponse({'detail_address':val[0],'name':val[1],'zipcode':val[2],'telphone':val[3],'addr_phone':val[4]})
def validate_addr(request):
    name = request.GET.get('name')
    addr = request.GET.get('addr')
    zipcode = request.GET.get('zipcode')
    telphone = request.GET.get('telphone')
    addr_phone = request.GET.get('addr_phone')
    user_name = request.GET.get('user_name')
    userid = User.objects.filter(user_email=user_name)[0].id # 查找当前用户的id
    res = TShoppingCart.objects.filter( userid=userid )  # 获取当前登录的用户,找到对应的购物车信息
    bookid_list = []  # 通过用户id，查询该用户添加了哪些书籍，将书籍id保存在列表中
    for j in res:
        bookid_list.append( j.bookid )
    re2 = TBook.objects.filter( id__in=bookid_list )  # 通过查出的书籍id获取这些书籍的信息

    cart_new = request.session.get( 'cart_new' ) # 获取购买的书籍
    if (not re2) and (not cart_new):
        return HttpResponse('error')
    else:
        shop_num = 0# 定义一个容器，存放商品的数量
        shop_id = []
        shopid = ''
        if cart_new == None:
            total_price = 0
        else:
            total_price = cart_new.sums()[0] # 计算商品总价
        s = '1234567890'
        str = random.sample(s,9)
        order_id = ''.join(str)+''.join(str) #生成随机订单号
        for i in cart_new.cart_items:# i 是一个个的 Cart_items对象
            shop_num += i.count # 商品数量
            shop_id.append(i.book.id)
        DOrderiterm.objects.create(shop_num=shop_num,total_price=total_price,order_id=order_id,userid=userid,shop_id=shop_id)
        # print(shop_num,type(shop_id),total_price,str)
        for i in cart_new.cart_items:# 将订单详情添加到t_order表中，需要数量，时间，价格，书籍id
            sum = i.count
            create_time = datetime.now()
            price = i.count*i.book.rel_price
            book_id = i.book.id
            TOrder.objects.create(num=sum,create_date=create_time,price=price,bookid=book_id)
            # cart_new.cart_items.remove(i)
            TShoppingCart.objects.filter(bookid=i.book.id).delete()

        re = TAddress.objects.filter(name=name,detail_address=addr,zipcode=zipcode,telphone=telphone,addr_phone=addr_phone,user_id=userid)
        if not re:
            TAddress.objects.create(name=name,detail_address=addr,zipcode=zipcode,telphone=telphone,addr_phone=addr_phone,user_id=userid)
        del request.session['cart_new']
        return JsonResponse({'order_id':order_id,'give_name':name,'items_sum':len(cart_new.cart_items),'total_price':total_price})
