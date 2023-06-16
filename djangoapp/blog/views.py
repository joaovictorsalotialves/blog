from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

from blog.models import Post, Page, Tag

PER_PAGE = 9


def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': 'Home - ',
        }
    )


def page(request, slug):
    _page = Page.objects.filter(is_published=True).filter(slug=slug).first()

    if _page is None:
        raise Http404()

    page_title = f'{_page.title} - Page - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page_obj': _page,
            'page_title': page_title,
        }
    )


def post(request, slug):
    _post = Post.objects.get_published().filter(slug=slug).first()

    if _post is None:
        raise Http404()

    page_title = f'{_post.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': _post,
            'page_title': page_title,
        }
    )


def created_by(request, author_pk):
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    posts = Post.objects.get_published().filter(created_by__pk=author_pk)

    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    page_title = user_full_name + 'posts - '

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].category.name} - Category - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    tag_title = Tag.objects.filter(slug=slug).first()

    if len(page_obj) == 0 or tag_title is None:
        raise Http404()

    page_title = f'{tag_title.name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published()
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    page_title = f'{search_value[:30]} - Search -'

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'search_value': search_value,
            'page_title': page_title,
        }
    )
