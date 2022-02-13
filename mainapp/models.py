from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=60,unique=True,verbose_name='Category name')
    description = models.TextField(blank=True,verbose_name='Category descrition')

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=70,verbose_name='Product name')
    image = models.ImageField(upload_to= 'products_images', blank=True)
    short_description = models.TextField(max_length=60,blank=True,verbose_name='products short description')
    description = models.TextField(max_length=250, blank=True,verbose_name='products description')
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0,verbose_name='products price')
    quantity = models.PositiveIntegerField(verbose_name='quantity of products available',default=0)


    def __str__(self):
        return self.name
