import pytest
from django.contrib.auth.models import User
from django.urls import reverse

USERNAME = 'newuser'
FIRST_NAME = 'newname'
LAST_NAME = 'newlastname'
PASSWORD1 = 'pass12345'
PASSWORD2 = 'pass12345'
UPDATE_USERNAME = 'updateuser'


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username=USERNAME,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        password=PASSWORD1,
    )
    return user


@pytest.fixture
def login_user(client, create_user):
    client.login(username=create_user.username, password=PASSWORD1)
    return create_user


@pytest.mark.django_db
def test_create_user(client):
    response = client.post(reverse('user_create'), {
        'username': USERNAME,
        'first_name': FIRST_NAME,
        'last_name': LAST_NAME,
        'password1': PASSWORD1,
        'password2': PASSWORD2,
    })
    assert response.status_code == 302
    assert User.objects.filter(username=USERNAME).exists()


@pytest.mark.django_db
def test_users_list(client, create_user):
    response = client.get(reverse('users_list'))
    assert response.status_code == 200
    assert create_user.username in response.content.decode()


@pytest.mark.django_db
def test_user_update(client, login_user):
    response = client.post(reverse('user_update',
                                   kwargs={'pk': login_user.pk}),
                           {'username': UPDATE_USERNAME, })
    assert response.status_code == 302
    login_user.refresh_from_db()
    assert login_user.username == UPDATE_USERNAME


@pytest.mark.django_db
def test_user_delete(client, login_user):
    response = client.post(reverse('user_delete',
                                   kwargs={'pk': login_user.pk}))
    assert response.status_code == 302
    assert not User.objects.filter(pk=login_user.pk).exists()
