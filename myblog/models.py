from django.db import models
import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publish')


class Article(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True)
    body = RichTextUploadingField()
    publish_time = models.DateTimeField(default=datetime.datetime.now)
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(max_length=100, choices=STATUS, default='draft')
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()
    published = PublishedArticleManager()

    def get_absolute_url(self):
        return reverse('myblog:article_detail', args=[self.id, self.slug])