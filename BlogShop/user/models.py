from django.db import models

class Reg(models.Model):
    nickname = models.CharField(max_length=20)
    first_name = models.CharField(max_length=40)
    second_name = models.CharField(max_length=40)
    email = models.EmailField()
    password = models.TextField()
    