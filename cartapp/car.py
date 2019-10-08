# coding:utf-8
#@Time : 2019/09/02  14:46
#author : Around
from testapp.models import TBook
class Cart_items():
    def __init__(self,book,count):
        # book是从数据库书籍详情表中查出来的QuerySet对象
        self.book = book
        self.count = count

class Cart():
    def __init__(self):
        self.total_price = 0
        self.save_price = 0
        # 列表存放的是Car_items对象
        self.cart_items = []
        self.del_items = []

    # 计算总价
    def sums(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.cart_items:
            self.total_price += i.book.rel_price * int(i.count)
            self.save_price += (i.book.original_cost-i.book.rel_price)*int(i.count)
        return self.total_price,self.save_price

    #增加商品
    def add_car(self,res,cont):
        for i in self.cart_items:#列表存放的是Car_items对象
            if i.book.id == res.id:
                i.count += int(cont)
                self.sums()
                return
        # self.cart_items.append(Cart_items(TBook.objects.filter(id=bookid)[0],count))
        self.cart_items.append(Cart_items(res,int(cont)))
        self.sums()


    #删除商品
    def del_car(self,bookid):
        for i in self.cart_items:
            if i.book.id == bookid:
                self.cart_items.remove(i)
                self.del_items.append(Cart_items(TBook.objects.filter(id=bookid),i.count))
                self.sums()

    #修改商品
    def change_nums(self,bookid,nums):
        for i in self.cart_items:
            if i.book.id == bookid:
                i.count = nums
                self.sums()

