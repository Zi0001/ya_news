from http import HTTPStatus
from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS

from news.models import Comment


FORM_DATA = {'text': 'Test'}


def test_anonimous_comment(client, new):
    initial_count = Comment.objects.count()
    url = reverse('news:detail', args=(new.pk,))
    client.post(url, FORM_DATA)
    assert Comment.objects.count() == initial_count


def test_auth_user_comment(author_client, new):
    initial_count = Comment.objects.count()
    url = reverse('news:detail', args=(new.pk,))
    author_client.post(url, FORM_DATA)
    assert Comment.objects.count() != initial_count


def test_user_cant_use_bad_words(author_client, new, comment):
    initial_count = Comment.objects.count()
    url = reverse('news:detail', args=(new.pk,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    author_client.post(url, data=bad_words_data)
    comments_count = Comment.objects.count()
    assert comments_count == initial_count


def test_auth_edit_comment(author_client, news, comment):
    url = reverse('news:edit', args=(news.pk,))
    author_client.post(url, data=FORM_DATA)
    news.refresh_from_db()
    comment_news = Comment.objects.get()
    assert comment_news.text == FORM_DATA['text']


def test_anonimous_edit_comment(client, new, comment):
    url = reverse('news:edit', args=(new.pk,))
    client.post(url, data=FORM_DATA)
    new.refresh_from_db()
    comment_news = Comment.objects.get()
    assert comment_news.text != FORM_DATA['text']


def test_author_can_delete_news(author_client, news, comment):
    initial_count = Comment.objects.count()
    url = reverse('news:delete', args=(news.pk,))
    response = author_client.post(url)
    expected_url = reverse('news:detail', args=(news.pk,))
    assertRedirects(response, f'{expected_url}#comments')
    assert Comment.objects.count() != initial_count


@pytest.mark.django_db
def test_anonimous_user_delete_news(client, news, comment):
    initial_count = Comment.objects.count()
    url = reverse('news:delete', args=(news.pk,))
    response = client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == initial_count
