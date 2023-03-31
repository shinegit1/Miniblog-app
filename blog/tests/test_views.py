import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertRedirects

from blog.models import Post


@pytest.mark.django_db
@pytest.mark.integration
def test_home_page(client):
    response = client.get("/")
    # assert that the user logged in if page redirected
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.integration
def test_signup_page(client):
    signup_url = '/signup/'
    data = {"first_name": "blog_2", "last_name": "user_2", "username": "bloguser2", "email": "bloguser2@gmail.com",
            "password1": "Password@123", "password2": "Password@123"}
    response = client.post(signup_url, data)
    # assert that user created account if redirected
    user = User.objects.get(username="bloguser2")
    expected_url = '/dash/'
    # assert that the user is authenticated if page redirected to dashboard
    assertRedirects(response, expected_url=expected_url, status_code=302, fetch_redirect_response=False)
    assert user.is_authenticated


@pytest.mark.django_db
@pytest.mark.integration
def test_login_page(client):
    login_url = '/login/'
    user = User.objects.get(username="bloguser1")
    data = {"username": "bloguser1", "password": "Password@123"}
    response = client.post(login_url, data)
    expected_url = '/dash/'
    # assert that the user is authenticated if page redirected to dashboard
    assertRedirects(response, expected_url=expected_url, status_code=302, fetch_redirect_response=False)
    assert user.is_authenticated


@pytest.mark.django_db
@pytest.mark.integration
def test_dashboard_page(client):
    posts = Post.objects.all()
    user = User.objects.get(pk=2)
    dash_url = '/dash/'
    client.login(username="bloguser1", password="Password@123")
    response = client.get(dash_url, {'posts': posts, 'full_name': user.get_full_name()})
    # assert that the authenticated user see all your blogs in the dashboard
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.integration
def test_add_blog(client):
    add_blog_url = "/add/"
    user = User.objects.get(username="bloguser1")
    client.login(username="bloguser1", password="Password@123")
    data = {"title": "Demo blog", "descript": "This is my blog."}
    response = client.post(add_blog_url, data)
    # assert that the authenticated user is added a new post
    assert response.status_code == 200
    assert Post.objects.filter(user=user, title="Demo blog")
