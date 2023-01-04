import pytest
from blog.models import Post

@pytest.mark.django_db
@pytest.mark.integration
def test_home_page(client):
    client.login(username="user1", password="Password@123")
    response =client.get("/")

    assert response.status_code == 200
