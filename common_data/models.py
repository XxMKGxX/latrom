from __future__ import unicode_literals

import json
import os
import copy

from django.db import models

from latrom import settings


class Person(models.Model):
    first_name = models.CharField(max_length =32)
    last_name = models.CharField(max_length =32)
    address = models.TextField(max_length =128, blank=True, default="")
    email = models.CharField(max_length =32, blank=True, default="")
    phone = models.CharField(max_length =16, blank=True, default="")

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

class SoftDeletionModel(models.Model):
    class Meta:
        abstract = True

    active = models.BooleanField(default=True)


    def delete(self):
        self.active = False
        self.save()

    def hard_delete(self):
        super().delete()

class Individual(Person, SoftDeletionModel):
    '''inherits from the base person class in common data
    represents clients of the business with entry specific details.
    the customer can also have an account with the business for credit 
    purposes
    A customer may be a stand alone individual or part of a business organization.
    '''
    phone_two = models.CharField(max_length = 16,blank=True , default="")
    other_details = models.TextField(blank=True, default="")
    organization = models.ForeignKey('common_data.Organization', 
        on_delete=models.CASCADE,null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    
  
    def __str__(self):
        return self.full_name


class Note(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, 
        null=True)
    note = models.TextField()

    def __str__(self):
        return "{}({}): {}".format(self.timestamp.strftime("%d %b %y, %H:%M "), self.author, self.note)

class Organization(models.Model):
    legal_name = models.CharField(max_length=255)
    business_address = models.TextField(blank=True)
    website = models.CharField(max_length=255, blank=True)
    bp_number = models.CharField(max_length=64, blank=True)
    email=models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    logo = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.legal_name

    @property 
    def members(self):
        return self.individual_set.all()

    def add_member(self, individual):
        individual.organization = self
        individual.save()
        

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class GlobalConfig(SingletonModel):
    DOCUMENT_THEME_CHOICES = [
        (1, 'Simple'),
        (2, 'Blue'),
        (3, 'Steel'),
        (4, 'Verdant'),
        (5, 'Warm')
    ]
    # TODO personalize email settings for each user
    email_host = models.CharField(max_length=32, blank=True, default="")
    email_port = models.IntegerField(null=True, blank=True)
    email_user = models.CharField(max_length=32, blank=True, default="")
    # TODO secure email password
    email_password = models.CharField(max_length=255, blank=True, default="")
    business_address = models.TextField(blank=True)
    logo = models.ImageField(null=True,upload_to="logo/", blank=True)
    document_theme = models.IntegerField(choices= DOCUMENT_THEME_CHOICES, 
        default=1)
    currency = models.ForeignKey('accounting.Currency', blank=True, 
        on_delete=models.SET_NULL, null=True)
    business_name = models.CharField(max_length=255, blank=True, default="")
    payment_details = models.TextField(blank=True, default="")
    contact_details = models.TextField(blank=True, default="")
    business_registration_number = models.CharField(max_length=32,blank=True, 
        default="")
    application_version = models.CharField(max_length=16, blank=True, default="0.0.1")

    

    def save(self, *args, **kwargs):
        super(GlobalConfig, self).save(*args, **kwargs)
        #serialize and store in json file so settings.py can access
        json_config = os.path.join(settings.BASE_DIR, 'global_config.json')
        with open(json_config, 'w+') as fil:
            fields = copy.deepcopy(self.__dict__)
            del fields['logo']
            del fields['_state']
            json.dump(fields, fil)

    @classmethod
    def logo_url(cls):
        conf = cls.objects.first()
        if conf and conf.logo:
            return conf.logo.url
        return ""