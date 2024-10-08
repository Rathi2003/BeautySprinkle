from django.db import models

class Detail(models.Model):
    name=models.CharField( max_length=50)
    email=models.CharField(max_length=100)
    address=models.TextField()
    contact=models.BigIntegerField()


class Example(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()


class Payment(models.Model):
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    amount = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)