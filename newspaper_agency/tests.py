from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import (
    Redactor,
    Topic,
    Newspaper,
    Commentary
)
from .forms import (
    RedactorCreationForm,
    RedactorLoginForm,
)


class ModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.redactor = Redactor.objects.create(
            username="redactor",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            years_of_experience=5,
        )
        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="This is a test newspaper content.",
            topic=self.topic,
        )
        self.newspaper.publishers.add(self.redactor)
        self.commentary = Commentary.objects.create(
            user=self.redactor,
            newspaper=self.newspaper,
            content="This is a test commentary.",
        )

    def test_topic_str(self):
        self.assertEqual(str(self.topic), "Test Topic")

    def test_redactor_str(self):
        self.assertEqual(str(self.redactor), "redactor (John Doe)")

    def test_newspaper_str(self):
        self.assertEqual(str(self.newspaper), "Test Newspaper")

    def test_comment_str(self):
        self.assertEqual(str(self.commentary), "This is a test commentary.")


class FormTest(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.valid_form = {
            "username": "testuser",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test",
            "last_name": "User",
            "years_of_experience": 5,
        }
        self.invalid_form = {
            "username": "testuser",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test",
            "last_name": "User",
            "years_of_experience": -5,
        }

    def test_redactor_creation_form_valid(self):
        form = RedactorCreationForm(data=self.valid_form)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_form_invalid(self):
        form = RedactorCreationForm(data=self.invalid_form)
        self.assertFalse(form.is_valid())

    def test_redactor_login_form_valid(self):
        form_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        form = RedactorLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_login_form_invalid(self):
        form_data = {
            "username": "",
            "password": "",
        }
        form = RedactorLoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        for i in range(10):
            Newspaper.objects.create(
                title=f"Newspaper {i}", content=f"Content {i}", topic=self.topic
            )

        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper", content="Test Content", topic=self.topic
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test123",
        )
        self.url = reverse("newspaper-agency:create-newspaper")
        self.newspaper_data = {
            "title": "Test Newspaper",
            "content": "Test Content",
        }

    def test_home_page_view(self):
        response = self.client.get(reverse("newspaper-agency:newspaper-home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_home.html")
        self.assertTrue("object_list" in response.context)
        self.assertTrue("title" in response.context)
        self.assertTrue("search_form" in response.context)
        self.assertTrue("topics" in response.context)

    def test_newspaper_detail_view(self):
        response = self.client.get(
            reverse(
                "newspaper-agency:newspaper-detail", kwargs={"pk": self.newspaper.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/newspaper_detail.html")
        self.assertTrue("newspaper" in response.context)
        self.assertEqual(response.context["newspaper"].title, "Test Newspaper")

    def test_create_newspaper_view(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.newspaper_data)
        self.assertEqual(response.status_code, 200)


class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("newspaper_agency:register")

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/register.html")
        self.assertIsInstance(response.context["form"], RedactorCreationForm)

    def test_register_post_invalid_form(self):
        response = self.client.post(self.register_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/register.html")
        self.assertIsInstance(response.context["form"], RedactorCreationForm)


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("newspaper_agency:login")
        self.user = Redactor.objects.create_user(
            username="test_user", password="password"
        )
        self.logout_url = reverse("newspaper_agency:logout")

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/login.html")
        self.assertIsInstance(response.context["form"], RedactorLoginForm)

    def test_login_post_valid_credentials(self):
        response = self.client.post(
            self.login_url, data={"username": "test_user", "password": "password"}
        )
        self.assertRedirects(response, reverse("newspaper_agency:newspaper-home"))

    def test_login_post_invalid_credentials(self):
        response = self.client.post(
            self.login_url, data={"username": "test_user", "password": "wrong_password"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/login.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)

    def test_login_post_invalid_form(self):
        response = self.client.post(self.login_url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "newspaper_agency/login.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)


class UserLogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse("newspaper_agency:logout")
        self.user = Redactor.objects.create_user(
            username="test_user", password="password"
        )

    def test_logout(self):
        self.client.login(username="test_user", password="password")
        self.assertTrue("_auth_user_id" in self.client.session)
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse("newspaper_agency:login"))
        self.assertFalse("_auth_user_id" in self.client.session)
