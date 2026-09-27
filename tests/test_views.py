import pytest
from django.urls import reverse
from promises.models import Tag, Promise

pytestmark = pytest.mark.django_db


@pytest.fixture
def promise():
    return Promise.objects.create(
        book="Philippians", chapter=4, verse_start=19,
        verse_ref="Philippians 4:19", verse_text="And my God will supply all your needs",
    )


def test_list_view_returns_200(client, promise):
    response = client.get(reverse("promises:list"))
    assert response.status_code == 200
    assert promise in response.context["promises"]


def test_detail_view_returns_200(client, promise):
    response = client.get(reverse("promises:detail", args=[promise.pk]))
    assert response.status_code == 200
    assert response.context["promise"] == promise


def test_search_view_with_query_matches(client, promise):
    response = client.get(reverse("promises:search"), {"q": "supply"})
    assert response.status_code == 200
    assert promise in response.context["promises"]


def test_search_view_without_query_returns_empty(client, promise):
    response = client.get(reverse("promises:search"))
    assert response.status_code == 200
    assert list(response.context["promises"]) == []


def test_by_tag_view_filters_correctly(client, promise):
    tag = Tag.objects.create(name="Provision & Finances", slug="provision", group=Tag.Group.CATEGORY)
    promise.tags.add(tag)
    other = Promise.objects.create(
        book="John", chapter=3, verse_start=16, verse_ref="John 3:16", verse_text="For God so loved..."
    )
    response = client.get(reverse("promises:by_tag", args=["category", "provision"]))
    assert promise in response.context["promises"]
    assert other not in response.context["promises"]
