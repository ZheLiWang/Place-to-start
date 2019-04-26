# -*- coding: utf-8 -*-
from django.db import models




class jingdong(models.Model): 
    name = models.CharField( max_length=255, blank=True, null=True)  
    phoneno = models.CharField( max_length=255, blank=True, null=True)  
    address = models.CharField( max_length=255, blank=True, null=True)  
    price = models.CharField( max_length=255, blank=True, null=True)
     

    class Meta:
        managed = True
        db_table = 'jingdong'

  

