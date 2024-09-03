# conftest.py
from django.conf import settings
import pytest

# Импортируем класс клиента.
from django.test.client import Client

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import Comment, News
from datetime import datetime, timedelta
from django.utils import timezone


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):  
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(  # Создаём объект заметки.
        title='Заголовок',
        text='Текст заметки',
    )
    Comment.objects.create(
        news=news,
        text='Текст комментария',
        author=author
    )
    return news


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def slug_for_args(news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.pk,)


@pytest.fixture
def page_home_count_news():
    today = datetime.today()
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
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news

@pytest.fixture
def comment(author):
    # comment = Comment.objects.create(
    #     news=news,
    #     author=author,
    #     text='Текст',
    # )
    # return comment
    return{
        'text':'Test',
    }
