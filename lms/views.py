from django.views.generic import TemplateView
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwner, IsModerator
from rest_framework.permissions import IsAdminUser


class HomePageView(TemplateView):
    template_name = "home.html"


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_permissions(self):
        # Настраиваем различные права доступа в зависимости от действия
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwner() | IsModerator()]
        elif self.action in ['create', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwner() | IsModerator()]
        elif self.action in ['create', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()


# class LessonCreateApiView(CreateAPIView):
#     serializer_class = LessonSerializer
#
#
# class LessonListApiView(ListAPIView):
#     serializer_class = LessonSerializer
#     queryset = Lesson.objects.all()
#
#
# class LessonRetrieveApiView(RetrieveAPIView):
#     serializer_class = LessonSerializer
#     queryset = Lesson.objects.all()
#
#
# class LessonUpdateApiView(UpdateAPIView):
#     serializer_class = LessonSerializer
#     queryset = Lesson.objects.all()
#
#
# class LessonDestroyApiView(DestroyAPIView):
#     queryset = Lesson.objects.all()