from django.test import TestCase
from rest_framework.test import APIClient

from lms.models import Course, Subscription
from users.models import User


class SubscriptionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.com", password="password")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", owner=self.user)

    def test_subscribe_and_unsubscribe(self):
        # Подписываемся на курс
        response = self.client.post(
            "/api/subscribe-to-course/", {"course_id": self.course.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вы успешно подписались на курс", response.data["message"])
        # Проверяем, что запись о подписке создана
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Отменяем подписку
        response = self.client.post(
            "/api/subscribe-to-course/", {"course_id": self.course.pk}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Подписка отменена", response.data["message"])
        # Проверяем, что запись о подписке была удалена
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
