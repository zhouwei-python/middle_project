# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    cate_name = models.CharField(max_length=20, blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    book_counts = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class DOrderiterm(models.Model):
    id = models.IntegerField(primary_key=True)
    shop_num = models.CharField(max_length=20, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    shop_id = models.CharField(max_length=50,blank=True, null=True)
    order_id = models.CharField(max_length=30,blank=True, null=True)
    userid = models.IntegerField( blank=True, null=True )

    class Meta:
        managed = False
        db_table = 'd_orderiterm'


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    telphone = models.CharField(max_length=20, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    addr_phone = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


class TBook(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=20, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    original_cost = models.IntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=20, blank=True, null=True)
    publish_time = models.DateField(blank=True, null=True)
    publish_version = models.CharField(max_length=20, blank=True, null=True)
    print_time = models.DateField(blank=True, null=True)
    print_version = models.CharField(max_length=20, blank=True, null=True)
    ibsn = models.CharField(db_column='IBSN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    word_number = models.CharField(max_length=20, blank=True, null=True)
    page_number = models.CharField(max_length=20, blank=True, null=True)
    book_size = models.CharField(max_length=20, blank=True, null=True)
    paper = models.CharField(max_length=20, blank=True, null=True)
    package = models.CharField(max_length=20, blank=True, null=True)
    author_intro = models.TextField(blank=True, null=True)
    catalogue = models.TextField(blank=True, null=True)
    media_comment = models.TextField(blank=True, null=True)
    rel_price = models.IntegerField(blank=True, null=True)
    editor_recommendation = models.TextField(blank=True, null=True)
    content_introduction = models.TextField(blank=True, null=True)
    chart_introduction = models.TextField( blank=True, null=True )
    digest_image_path = models.CharField(max_length=2000, blank=True, null=True)
    product_image_path = models.CharField(max_length=2000, blank=True, null=True)
    series_name = models.CharField(max_length=128, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    shelves_date = models.DateField(blank=True, null=True)
    customer_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    book_status = models.IntegerField(blank=True, null=True)
    sales = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    comment = models.IntegerField()
    suite = models.SmallIntegerField()
    title1 = models.CharField(max_length=300,null=True)
    title2 = models.CharField(max_length=300,null=True)
    cate_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 't_book'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    num = models.CharField(max_length=20, blank=True, null=True)
    create_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    bookid = models.IntegerField(blank=True,null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TShoppingCart(models.Model):
    id = models.IntegerField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    bookid = models.IntegerField(blank=True, null=True)
    column_6 = models.CharField(db_column='Column_6', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_shopping_cart'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_email = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)
    user_status = models.IntegerField(blank=True, null=True)
    user_prefix = models.CharField(max_length=10,blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'user'
