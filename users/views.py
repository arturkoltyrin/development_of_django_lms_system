from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from users.serializers import UserSerializer
from .models import Payment, User
from .serializers import PaymentSerializer
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView)
from users.permissions import IsOwner, IsModerator
from lms.serializers import CourseSerializer
from lms.models import Course
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('paid_course','paid_lesson','type',)
    ordering_fields = ('payment_date',)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsModerator]

class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner, IsModerator]

class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsModerator]


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get('course_id')
        course = Course.objects.all().get(id=course_id)
        course_title = course.title
        course_price = course.price
        stripe_product_id = create_stripe_product(course_title)
        stripe_price = create_stripe_price(stripe_product_id, course_price)
        session_id, payment_link = create_stripe_session(stripe_price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

