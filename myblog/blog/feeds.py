import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LastPostsFeed(Feed):
    title = 'My Blog'
    # reverse_lazy to generate url for link attrbute
    # reverse method to build urls by their name and pass optional params
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog'

    def items(self):
        return Post.publish_objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdated(self, item):
        return item.published
