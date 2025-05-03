from django.core.management.base import BaseCommand
from users.models import Payment, User
from lms.models import Course, Lesson


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Создаём суперпользователя
        params = dict(email="admin@example.com", password="Zx1234567890")
        user, user_created = User.objects.get_or_create(**params)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("Superuser created successfully."))

        # Создаём тестовые курсы
        course1 = Course.objects.create(title="Test Course 1", description="This is test course number one.", preview="test_preview.jpg")
        course2 = Course.objects.create(title="Test Course 2", description="This is test course number two.", preview="test_preview.jpg")

        # Создаём тестовые уроки
        lesson1 = Lesson.objects.create(title="Test Lesson 1", description="First lesson", course=course1, video_url="https://example.com/video1.mp4")
        lesson2 = Lesson.objects.create(title="Test Lesson 2", description="Second lesson", course=course2, video_url="https://example.com/video2.mp4")

        # Создаём платежи
        Payment.objects.create(owner=user, payment_date="2023-10-01", paid_course=course1, amount=100.00, type="CASH")
        Payment.objects.create(owner=user, payment_date="2023-10-02", paid_course=course2, amount=150.00, type="BANK_TRANSFER")
        Payment.objects.create(owner=user, payment_date="2023-10-03", paid_lesson=lesson1, amount=50.00, type="CASH")
        Payment.objects.create(owner=user, payment_date="2023-10-04", paid_lesson=lesson2, amount=75.00, type="BANK_TRANSFER")

        self.stdout.write(self.style.SUCCESS("All data loaded successfully!"))