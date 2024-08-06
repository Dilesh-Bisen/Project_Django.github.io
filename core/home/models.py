from django.db import models
from django.db.models.signals import post_save, post_delete, post_init, post_migrate
from django.dispatch import receiver
import os
# Create your models here.


class Student(models.Model):
    # id = models.AutoField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)


class Car(models.Model):
    car_name = models.CharField(max_length=500)
    speed = models.IntegerField(default=50)

    def __str__(self) -> str:
        return self.car_name


@receiver(post_save, sender=Car)
def call_car_api(sender, instance, **kwargs):
    print("Car Object Created")
    print(sender, instance, kwargs)
