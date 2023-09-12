from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
# Create your views here.


# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(data=request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             # fields to search in
#             search_vector = SearchVector(
#                 'title', weight='A', config='spanish') +\
#                 SearchVector('body', weight='B', config='spanish')
#             #  config='spanish' to remove stop words in spanish
#             search_query = SearchQuery(query, config='spanish')
#             '''
#             Filters the search results based on the search query
#             and orders the results by descending relevance rank
#             ----------------------------------------------------
#             Usage with SearchVector: SearchQuery is typically used in
#             combination with SearchVector to perform full-text search in Django
#             '''
#             results = Post.publish_objects.annotate(
#                 search=search_vector,
#                 rank=SearchRank(search_vector, search_query)
#             ).filter(search=search_query).order_by('-rank')

#     return render(request, 'blog/post/search.html', {'form': form,
#                                                      'query': query,
#                                                      'results': results})


# search with trigram
def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.publish_objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


def post_list(request, tag_slug=None):

    post_list = Post.publish_objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # make init from Paginator with max num of posts in page
    paginator = Paginator(post_list, 3)
    # return the paginated page from req by default = 1
    page_number = request.GET.get('page', 1)
    try:
        # pass page_number to paginator.page() which returns the page object
        # with stored posts
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_num in url is passed string not int
        posts = paginator.page(1)
    except EmptyPage:
        # if page_num is out of range in url deliver last page of results
        posts = paginator.page(paginator.num_pages)

    form = CommentForm()
    return render(request, 'blog/post/list.html', {'posts': posts, 'form': form, 'tag': tag})


# another way to make list view by class based views
# but it returns http404 if page is string or out of range
class PostListView(ListView):
    queryset = Post.publish_objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list2.html'


def post_detail(request, year, month, day, post):
    #    post = get_object_or_404(Post,id=id,status = Post.Status.PUBLISHED)
    # removing id from url of post_datil to make seo friendly url
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED,
                             slug=post,
                             published__year=year,
                             published__month=month,
                             published__day=day)
    # comments from related_name = comments in models.py
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # list of similar posts
    post_tags_ids = post.tags.values_list(
        'id', flat=True)  # flat to return list not tuples
    published_posts = Post.publish_objects.all()
    similar_posts = published_posts.filter(
        tags__in=post_tags_ids).exclude(id=post.id)  # exclude the post itself
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-published')[:4]
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'form': form,
                                                     'similar_posts': similar_posts})


def email_post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            '''After the form data has been validated, you can access the cleaned form 
            input data through the form.cleaned_data attribute. 
            This attribute provides a dictionary where the keys are the field names defined in the form,
            and the values are the cleaned and validated values entered by the user
            '''
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends your read"\
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                f"{cd['name']} \'s comments: {cd['comments']}"
            send_mail(subject, message,
                      'abdelrhmanmamdouh776@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post,
                                                      'form': form,
                                                      'comment': comment})
