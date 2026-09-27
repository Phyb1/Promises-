import pytest
from promises.models import Tag, Promise

pytestmark = pytest.mark.django_db


def make_promise(ref="Philippians 4:19", text="And my God will supply..."):
    return Promise.objects.create(
        book=ref.split()[0], chapter=4, verse_start=19, verse_ref=ref, verse_text=text
    )


def test_promise_str_returns_verse_ref():
    assert str(make_promise()) == "Philippians 4:19"


def test_search_matches_verse_text():
    make_promise(text="Do not be anxious about anything")
    assert Promise.objects.search("anxious").count() == 1


def test_search_matches_tag_name():
    promise = make_promise()
    tag = Tag.objects.create(name="Provision & Finances", slug="provision", group=Tag.Group.CATEGORY)
    promise.tags.add(tag)
    assert Promise.objects.search("provision").count() == 1


def test_search_no_match_returns_empty():
    make_promise()
    assert Promise.objects.search("nonexistent").count() == 0


def test_in_group_filters_by_tag_group():
    promise = make_promise()
    promise.tags.add(Tag.objects.create(name="Morning", slug="morning", group=Tag.Group.TIME))
    assert Promise.objects.in_group(Tag.Group.TIME).count() == 1
    assert Promise.objects.in_group(Tag.Group.CATEGORY).count() == 0


def test_tag_slug_unique_within_group():
    Tag.objects.create(name="Morning", slug="morning", group=Tag.Group.TIME)
    with pytest.raises(Exception):
        Tag.objects.create(name="Morning Dup", slug="morning", group=Tag.Group.TIME)
