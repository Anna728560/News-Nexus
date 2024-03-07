from django.test import TestCase
from .models import Topic, Redactor, Newspaper


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


