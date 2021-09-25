from django.db import models

# Create your models here.
class Product(models.Model):
    # product_id = models.BigIntegerField(primary_key = True)
    product_id = models.AutoField
    product_name = models.CharField(max_length=70)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to = "shop/images",default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=50 , default="")
    email  = models.CharField(max_length=254 , default="")
    phone = models.CharField(max_length=50,default="")
    desc  = models.CharField(max_length=500 , default="")
    msg_date = models.DateField()

    def __str__(self):
        return self.name
