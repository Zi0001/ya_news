from django.urls import reverse
import pytest

from news.forms import CommentForm


@pytest.mark.django_db
def test_count_news(client, page_home_count_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert len(object_list) == len(page_home_count_news)


@pytest.mark.django_db
def test_sort_news(client, page_home_count_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
def test_sort_comment(client, name, args, comments_detail_news):
    url = reverse(name, args=args)
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
def test_anonymous_client_form(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert 'form' not in response.context


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_for_args')),
    )
)
def test_authorized_client_form(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
