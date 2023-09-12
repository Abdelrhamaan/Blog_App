from django.contrib.sitemaps import Sitemap
from .models import Post

# to create url for each post in blog with your domain name


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.publish_objects.all()

    def lastmod(self, obj):
        return obj.updated
