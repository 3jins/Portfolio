from django.db import models
from django.utils import timezone


class AdminInfo(models.Model):
    admin_id = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    admin_pw = models.CharField(max_length=32, blank=False, null=False) # md5 hash
    admin_lv = models.IntegerField(blank=False, null=False)    # 1 : highest
    fails = models.IntegerField(default=0)
    fail_time = models.DateTimeField(default='2000-01-01 00:00:00.000')


class Menu(models.Model):
    menu_code = models.IntegerField(blank=False, null=False, primary_key=True)
    menu_title = models.CharField(max_length=20, blank=False, null=False)
    submenu_title = models.CharField(max_length=20, blank=True, null=True)


class Content(models.Model):
    # content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    thumbnail_pic = models.CharField(max_length=200, blank=True, null=True)
    thumbnail_text = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    menu = models.ForeignKey(Menu, db_column='menu_code')


class Context(models.Model):
    seq = models.IntegerField(blank=False, null=False)
    content = models.ForeignKey(Content)
    context = models.CharField(max_length=10000, blank=True, null=True) # Can store about 100,000 contents in 1GB.
    type = models.SmallIntegerField(blank=False, null=False)    # 1:subtitle 2:text 3:image 4:clip


class Commentor(models.Model):
    email = models.CharField(max_length=100, blank=False, null=False, primary_key=True)   # g/jinaidy93@gmail.com, f/jinaidy
    name = models.CharField(max_length=30, blank=False, null=False, default='static/Portfolio/img/comment/commentor/default.png')
    picture = models.CharField(max_length=200)

        # def is_there_that_commentor(email, self):
        #     if self.objects.filter(email=email).first() is None:
        #         return False
        #     else:
        #         return True


class Comment(models.Model):
    comment = models.CharField(max_length=10000, blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)
    edit_date = models.DateTimeField(default=0, blank=True, null=True)
    commentor = models.ForeignKey(Commentor, db_column='commentor_email')
    content = models.ForeignKey(Content)


class GoogleAccessToken(models.Model):
    email = models.CharField(max_length=100, blank=False, null=False, primary_key=True)
    refresh_token = models.CharField(max_length=100, blank=False, null=False)