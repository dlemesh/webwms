import datetime
import json
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    sdid = models.CharField(max_length=200)
	
    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'web_client'
        
class ReferredClients(models.Model):
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)

class Sku(models.Model):
    id = models.IntegerField(primary_key=True)
    sku_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
    sdid = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'web_sku'
    
class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    sdid = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
    client_name = models.CharField(max_length=200)
    date_to_ship = models.DateTimeField()
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.display_name

    class Meta:
        managed = False
        db_table = 'web_order'

class OrderDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Order)
    line = models.IntegerField()
    sku = models.ForeignKey(Sku)
    sku_name = models.CharField(max_length=200)
    qty = models.IntegerField()
    planned = models.IntegerField()
    moved = models.IntegerField()
    packed = models.IntegerField()
    shiped = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'web_order_detail'

class Incoming(models.Model):
    id = models.IntegerField(primary_key=True)
    sdid = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    holder = models.ForeignKey(Client)
    client_name = models.CharField(max_length=200)
    date_to_ship = models.DateTimeField()
    status = models.CharField(max_length=200)
	
    def __str__(self):
        return self.display_name

    class Meta:
        managed = False
        db_table = 'web_incoming'

class IncomingDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    inc = models.ForeignKey(Order)
    line = models.IntegerField()
    sku = models.ForeignKey(Sku)
    sku_name = models.CharField(max_length=200)
    qty = models.IntegerField()
    received = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'web_incoming_detail'