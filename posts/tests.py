from django.test import TestCase
from django.urls import reverse

from datetime import datetime, timezone

from .models import Post


def create_post(title, text="Test Post", draft=False, publication_date=None):
    """
    Create a new `Post`.
    """
    if not publication_date:
        publication_date = datetime.now(timezone.utc)
    return Post.objects.create(
        title=title, text=text, draft=draft, publication_date=publication_date
    )


class PostIndexViewTests(TestCase):
    def test_no_posts(self):
        """
        If no `Post`s exist, a specific message is displayed.
        """
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No posts published yet.")
        self.assertQuerysetEqual(response.context["published_posts"], [])

    def test_list_published_posts(self):
        """
        List published `Post`s and no `Post`s with `draft==True`.
        """
        create_post("Test Post 1")
        create_post("Test Post 2")
        create_post("Test Post 3", draft=True)
        create_post("Test Post 4")
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post 1")
        self.assertContains(response, "Test Post 2")
        self.assertNotContains(response, "Test Post 3")
        self.assertContains(response, "Test Post 4")

    def test_newer_posts_come_first(self):
        """
        List more recent `Post`s at the top.
        """
        old = create_post(
            "Old post", publication_date=datetime(2010, 1, 1, 0, 0, 0, 0, timezone.utc)
        )
        recent = create_post(
            "Recent post", publication_date=datetime(2020, 1, 1, 0, 0, 0, 0, timezone.utc)
        )
        vold = create_post(
            "Very old post", publication_date=datetime(2000, 1, 1, 0, 0, 0, 0, timezone.utc)
        )
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["published_posts"], [repr(recent), repr(old), repr(vold)]
        )


class PostDetailViewTests(TestCase):
    def test_view_post(self):
        """
        A `Post` can be viewed and its contained markdown is rendered properly.
        """
        content = (
            "# Big headline\n"
            "hi\n"
            "## smaller headline\n"
            "hello `code`\n"
        )
        post = create_post("Test Post 1", text=content)
        response = self.client.get(reverse("posts:detail", args=(post.id,)))
        self.assertEqual(response.status_code, 200)
        expected = (
            "<h1>Big headline</h1>\n"
            "<p>hi</p>\n"
            "<h2>smaller headline</h2>\n"
            "<p>hello <code>code</code></p>"
        )
        self.assertContains(response, expected)

    def test_cant_view_draft_posts(self):
        """
        A `Post` with `draft==True` can't be viewed and will return 404.
        """
        post = create_post("Test Post 1", draft=True)
        response = self.client.get(reverse("posts:detail", args=(post.id,)))
        self.assertEqual(response.status_code, 404)
