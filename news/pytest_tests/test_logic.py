from django.urls import reverse
import pytest
from news.forms import CommentForm

from news.forms import BAD_WORDS, WARNING

from news.models import Comment, News


def test_anonimous_comment(client, new, comment):
    url = reverse('news:detail', args=(new.pk,))
    client.post(url, comment)
    assert Comment.objects.count() == 0


def test_auth_user_comment(author_client, new, comment):
    url = reverse('news:detail', args=(new.pk,))
    author_client.post(url, comment)
    assert Comment.objects.count() == 1


def test_user_cant_use_bad_words(author_client, new):
    url = reverse('news:detail', args=(new.pk,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    author_client.post(url, data=bad_words_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_auth_edit_comment(author_client, news):
    url = reverse('news:edit', args=(news.pk,))
    form_data = {'text':'Test'}
    author_client.post(url, data=form_data)
    news.refresh_from_db()
    coun = Comment.objects.count()
    assert coun == 1


def test_anonimous_edit_comment(client, new):
    url = reverse('news:edit', args=(new.pk,))
    form_data = {'text':'Test'}
    client.post(url, data=form_data)
    new.refresh_from_db()
    assert Comment.objects.count() == 0
