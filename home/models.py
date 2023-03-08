from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name    

class Product(models.Model):
        name = models.CharField(max_length = 200)
        price = models.IntegerField(max_length = 200)
        category = models.ForeignKey(Category,on_delete=models.CASCADE)
        image = models.ImageField(upload_to ='products')
        user = models.ForeignKey(User, on_delete=models. CASCADE,null=True)
        def __str__(self):
            return self.name   


class Post(models.Model):
      title = models.CharField(max_length= 200) 
      description = models.TextField()
      image = models.ImageField  (upload_to= "post")   

      def __str__(self):
        return self.title     

      def get_absolute_url(self):
           return reverse("viewpost", kwargs={"pk": self.pk})                   
           
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(decimal_places=2, max_digits=8)
    created_at = models.DateTimeField(auto_now_add=True)    
