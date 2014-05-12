#coding: utf-8

from django.db import models

# Create your models here.

class Catalog(models.Model):
    name = models.CharField(max_length = 64)
    desc = models.CharField(max_length = 512, null=True)
    
    #1 ²©¿Í 2 ÓÎÏ·
    type = models.IntegerField()
    
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    def __unicode__(self):
        return '<cat:' + self.name + '>'

class Label(models.Model):
    name = models.CharField(max_length = 32)
    desc = models.CharField(max_length = 512, null=True)
    
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    
    def __unicode__(self):
        return '<label:' + self.name + '>'

class Archive(models.Model):
    year = models.CharField(max_length = 8)
    month = models.CharField(max_length = 4)

    def __unicode__(self):
        return '<' + self.year + '-' + self.month + '>'

class Passage(models.Model):
    title = models.CharField(max_length = 128)
    content = models.TextField()
    summary = models.TextField(null=True)    
    hot = models.IntegerField()
    
    visiable = models.BooleanField()
    enable_comment = models.BooleanField()    
    front_flag = models.BooleanField()
    
    draft_flag = models.BooleanField()
    
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    catalog = models.ForeignKey(Catalog, null=True)
    labels = models.ManyToManyField(Label)
    archive = models.ForeignKey(Archive)

    def __unicode__(self):
        return '<passage:' + self.title + '>'
        
class Comment(models.Model):
    author = models.CharField(max_length = 64)
    email = models.EmailField()  
    site = models.CharField(max_length = 256, null=True)
    image = models.CharField(max_length = 64)
    content = models.TextField()    
    ip_address = models.IPAddressField()
    is_notify = models.BooleanField()
    create_time = models.DateTimeField()
    
    passage = models.ForeignKey(Passage)
    parent = models.ForeignKey('self', null=True)

    def __unicode__(self):
        return '<comment:' + self.author + '>'

class Settings(models.Model):
    title = models.CharField(max_length = 128)
    brand = models.CharField(max_length = 128)
    copy_info = models.CharField(max_length = 256)
    
    #blog setting
    blog_display_count = models.IntegerField()
    blog_notify = models.BooleanField()
    blog_overview = models.BooleanField()
  
    #game setting
    game_menu_count = models.IntegerField()
    
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()


    def __unicode__(self):
        return '<settings:' + self.title + '>'
        
class Module(models.Model):
    name = models.CharField(max_length = 64)
    desc = models.CharField(max_length = 512, null=True)
    
    #setting
    visiable = models.BooleanField()
    display_count = models.IntegerField()
    
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    def __unicode__(self):
        return '<module:' + self.name + '>'
class Game(models.Model):
    name = models.CharField(max_length = 64)
    desc = models.CharField(max_length = 512, null=True)
    image = models.CharField(max_length = 128)
    width = models.IntegerField()
    height = models.IntegerField()
    visiable = models.BooleanField()    
    #statistic
    hot = models.IntegerField()
    
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    
    catalog = models.ForeignKey(Catalog, null=True)

    def __unicode__(self):
        return '<game:' + self.name + '>'
        
        