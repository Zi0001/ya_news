from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from django.urls import reverse
import pytest

# @pytest.mark.django_db
# def test_home_anonymous_user(client):
#     url = reverse('news:home')
#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('slug_for_args')),
        ('users:login', None),
        ('users:logout', None)
    )
)
@pytest.mark.django_db
def test_detail(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
@pytest.mark.django_db
def test_delete_edit_auth_user(author_client, name, news):
    url = reverse(name, args=(news.pk,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
@pytest.mark.django_db
def testredirects_login(client, name, news):
    login_url = reverse('users:login')
    url = reverse(name, args=(news.pk,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit'),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, news, expected_status
):
    url = reverse(name, args=(news.pk,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
