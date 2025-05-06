from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course, Lesson

class LessonAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', password='password')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test Course', owner=self.user)
        self.lesson_data = {
            'title': 'Test Lesson',
            'description': 'Описание урока',
            'video_url': 'https://www.youtube.com/watch?v=test123',
            'owner': self.user
        }
        self.lesson = Lesson.objects.create(course=self.course, **self.lesson_data)

    def test_create_lesson(self):
        response = self.client.post('/api/lessons/', {
            'title': 'New Lesson',
            'description': 'Описание урока',
            'video_url': 'https://www.youtube.com/watch?v=test123',
            'course': self.course.pk,
            'owner': self.user.pk
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_list_lessons(self):
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_lesson(self):
        lesson = Lesson.objects.create(course=self.course, **self.lesson_data)
        response = self.client.get(f'/api/lessons/{lesson.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(course=self.course, **self.lesson_data)
        updated_data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/lessons/{lesson.pk}/', updated_data)
        self.assertEqual(response.status_code, 200)
