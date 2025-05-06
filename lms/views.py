from django.views.generic import TemplateView
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from rest_framework.permissions import SAFE_METHODS
from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwner, IsModerator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .paginators import StandardResultsSetPagination
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


class HomePageView(TemplateView):
    template_name = "home.html"

class IsNotModeratorOrReadOnly(IsModerator):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.method in SAFE_METHODS


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated, IsNotModeratorOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.none()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner,  IsModerator]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SubscribeToCourse(APIView):
    def post(self, request, format=None):
        course_id = request.data.get('course_id')
        try:
            course = get_object_or_404(Course, pk=course_id)
        except Http404:
            return Response({'error': 'Указанный курс не существует'}, status=404)
        subscription = Subscription.objects.filter(user=request.user, course=course)
        if subscription.exists():
            subscription.delete()
            message = 'Подписка отменена'
        else:
            Subscription.objects.create(user=request.user, course=course)
            message = 'Вы успешно подписались на курс'
        return Response({'message': message}, status=200)





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