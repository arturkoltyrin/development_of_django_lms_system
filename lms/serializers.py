from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_link

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["title"]


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    def get_is_subscribed(self, obj):
        """Возвращает true, если текущий пользователь подписан на курс"""
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return False
        return bool(Subscription.objects.filter(user=user, course=obj).first())
    class Meta:
        model = Course
        fields = ("id", "title", "description", "preview", "is_subscribed")

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            {"video_url": validate_youtube_link}
        ]