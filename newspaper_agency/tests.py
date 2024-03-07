from multiprocessing.connection import Client

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase
from .models import Redactor, Topic, Newspaper
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RedactorCreationForm, RedactorLoginForm, NewspaperForm, TopicSearchForm


class ModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.redactor = Redactor.objects.create(
            username="redactor",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            years_of_experience=5
        )
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="This is a test newspaper content.",
            topic=self.topic
        )
        self.newspaper.publishers.add(self.redactor)

    def test_topic_str(self):
        self.assertEqual(str(self.topic), "Test Topic")

    def test_redactor_str(self):
        self.assertEqual(
            str(self.redactor),
            "redactor (John Doe)"
        )

    def test_newspaper_str(self):
        self.assertEqual(str(self.newspaper), "Test Newspaper")


class RedactorCreationFormTest(TestCase):
    def test_redactor_creation_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password1': 'test12345',
            'password2': 'test12345',
            'first_name': 'Test',
            'last_name': 'User',
            'years_of_experience': 5,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_valid_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'test12345',
            'password2': 'test12345',
            'first_name': 'Test',
            'last_name': 'User',
            'years_of_experience': 5,
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class RedactorLoginFormTest(TestCase):
    def test_redactor_login_form_invalid(self):
        form_data = {
            'username': '',
            'password': '',
        }
        form = RedactorLoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class HomePageViewTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        for i in range(10):
            Newspaper.objects.create(title=f"Newspaper {i}", content=f"Content {i}", topic=self.topic)

    def test_home_page_view(self):
        response = self.client.get(reverse("newspaper-agency:newspaper-home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_home.html")
        self.assertTrue("object_list" in response.context)
        self.assertTrue("title" in response.context)
        self.assertTrue("search_form" in response.context)
        self.assertTrue("topics" in response.context)


class NewspaperDetailViewTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.newspaper = Newspaper.objects.create(title="Test Newspaper", content="Test Content", topic=self.topic)

    def test_newspaper_detail_view(self):
        response = self.client.get(reverse("newspaper-agency:newspaper-detail", kwargs={"pk": self.newspaper.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_detail.html")
        self.assertTrue("newspaper" in response.context)
        self.assertEqual(response.context["newspaper"].title, "Test Newspaper")


class CreateNewspaperViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.url = reverse("newspaper-agency:create-newspaper")
        self.newspaper_data = {
            "title": "Test Newspaper",
            "content": "Test Content",
        }

    def test_create_newspaper_view(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.newspaper_data)
        self.assertEqual(response.status_code, 200)
