from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.


class PublishedManger(models.Manager):
    # inherit from models.manager then ovveride the method to make object instead of return
    # Post.objects.all()  ----> Post.published.all() and so on

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class DraftedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.DRAFT)


# ---------- post model --------------
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'PUBLISHED'

    title = models.CharField(max_length=250)
    # to ensure that there is no two slugs have the same slug at the same date
    slug = models.SlugField(max_length=250, unique_for_date='published')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(
        auto_now_add=True)  # when obj is first created
    updated = models.DateTimeField(auto_now=True)  # when obj is last saved
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)
    # related_name to allow access related objects to user by user.blog_posts
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')

    objects = models.Manager()  # default manager
    publish_objects = PublishedManger()  # our custom manager
    drafts_objects = DraftedManager()  # our custom manager
    tags = TaggableManager()  # tag custom manager

    class Meta:
        ordering = ['-published']
        # to improve performance
        indexes = [models.Index(fields=['-published'])]

    def __str__(self):
        return self.title

    # removing id from url of post_datil to make seo friendly url
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.published.year,
                                                 self.published.month,
                                                 self.published.day,
                                                 self.slug])


# ---------- comment model --------------
class Comment(models.Model):
    '''
    related name post.comments.all()
    by deafult django made ir post.comment_set.all()
    '''
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created']),]

    def __str__(self) -> str:
        return f'Comment by {self.name} on {self.post}'
