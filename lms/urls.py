from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonViewSet, HomePageView,SubscribeToCourse)

app_name = LmsConfig.name
router = SimpleRouter()
router.register("courses", CourseViewSet)
router.register("lessons", LessonViewSet)

urlpatterns = [path("", HomePageView.as_view(), name="home"),
               path('subscribe-to-course/', SubscribeToCourse.as_view(), name='subscribe-to-course'),
               ]

urlpatterns += router.urls