from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

#  you can use the name of function or name='all_posts'

# create simple tag to return number of publishe posts


@register.simple_tag(name='all_posts')
def total_posts():
    return Post.publish_objects.count()

# create simple tag to return number of posts have most comments


@register.simple_tag(name='most_commented')
def get_most_commented_posts(count=4):
    # published_posts = Post.published.all()
    most_commented = Post.publish_objects.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]
    return most_commented

# create inclusion tag to return number of latest posts


@register.inclusion_tag('blog/post/latest.html')
def latest_posts(count=5):
    latest_posts = Post.publish_objects.order_by('-published')[:count]
    return {'latest_posts': latest_posts}

#  create templ. filter to support markdown syntax


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
