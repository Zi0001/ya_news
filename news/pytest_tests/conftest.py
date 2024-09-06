from django.conf import settings
import pytest

from django.test.client import Client

from news.models import Comment, News
from datetime import timedelta
from django.utils import timezone


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',

    )

    # Comment.objects.create(
    #     news=news,
    #     text='Текст комментария',
    #     author=author
    # )
    return news


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        text='Текст комментария',
        author=author
    )


@pytest.fixture
def pk_for_args(news):
    return (news.pk,)


@pytest.fixture
def page_home_count_news():
    today = timezone.now()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def comments_detail_news(news, author):
    now = timezone.now()

    for index in range(3):
        comment = Comment.objects.create(
            text=f'Текст {index}',
            news=news,
            author=author,
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def new(author):
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
