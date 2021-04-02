from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from extensions.utils import jalali_convertor


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)
    position = models.IntegerField()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ('position',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('myblog:category', args=[self.slug])


class PublishedArticleManager(models.Manager):
    def published(self):
        return self.filter(status='publish')


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class Article(models.Model):
    STATUS = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )
    title = models.CharField(max_length=120, verbose_name='عنوان')
    slug = models.SlugField(max_length=120, unique=True)
    body = RichTextUploadingField(blank=True, null=True, verbose_name='بدنه مقاله')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته بندی')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=STATUS, default='draft', verbose_name='وضعیت')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    objects = PublishedArticleManager()
    hits = models.ManyToManyField(IPAddress, blank=True, through='ArticleHit', related_name='hits')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def jpublish(self):
        return jalali_convertor(self.publish_time)
    jpublish.short_description = 'زمان انتشار'

    def get_absolute_url(self):
        return reverse('myblog:article_detail', args=[self.id, self.slug])

    def category_published(self):
        return self.category.filter(status=True)


# to fetch most seen articles of month
class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)








