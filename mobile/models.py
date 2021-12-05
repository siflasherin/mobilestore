from django.db import models
# from mobile.models import Mobile
from django.contrib.auth.models import User

# Create your models here.
class Mobile(models.Model):
    mobile_name=models.CharField(max_length=100)
    model=models.CharField(unique=True,max_length=100)
    colour=models.CharField(max_length=100)
    storage=models.PositiveIntegerField(max_length=3)
    copies=models.PositiveIntegerField(max_length=100)
    price=models.PositiveIntegerField(max_length=100,default=100)
    image=models.ImageField(upload_to="images",null=True)

    def __str__(self):
        return self.mobile_name


class Cart(models.Model):
    item=models.ForeignKey(Mobile,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("incart","incart"),
        ("cancelled","cancelled"),
        ("order placed","order placed")
    )
    status=models.CharField(max_length=100,choices=options,default="incart")

class Orders(models.Model):
    item=models.ForeignKey(Cart,on_delete=models.CASCADE)
    user=models.CharField(max_length=40)
    address=models.CharField(max_length=100)
    order_date=models.DateField(auto_now_add=True)
#     orderplaced,dispatch,order_cancelled,delivered,intransit
    options=(
        ("orderplaced","orderplaced"),
        ("dispatch","dispatch"),
        ("intransit","intransit"),
        ("delivered","delivered"),
        ("order_cancelled","order_cancelled")
    )
    status=models.CharField(max_length=100,choices=options,default="orderplaced")
    delivery_date=models.DateField(null=True,blank=True)
# book=Book()
# print(Book)

# ORM queries
# python3 manage.py shell
# from mobile.models import Mobile
# book=Book.objects.create(mobile_name="HUWEI",model="model1",colour="red",storage=36,copies=50,price=50000)
# mobile=Mobile.objects.create(mobile_name="HUWEI",model="model1",colour="red",storage=36,copies=50,price=50000)
# mobile.save()
# mobiles=Mobile.objects.all()
# mobiles
# mobiles=Mobile.objects.filter(price__gt=30000)
# for mobile in mobiles:
# ...     print(mobile.mobile_name,mobile.colour)
# ...
# mobiles=Mobile.objects.filter(price__gt=10000,price__lte=50000)
#mobiles=Mobile.objects.filter(mobile_name__iexact="samsung")
#mobiles=Mobile.objects.filter(mobile_name__contains="hu")
# mobile=Mobile.objects.get(id=3)
# mobile.delete()  -----  (1, {'mobile.Mobile': 1})

# mobiles=Mobile.objects.all().values('id','mobile_name')










