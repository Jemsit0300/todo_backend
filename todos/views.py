from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend


# ToDo CRUD API
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # Men gosdum
    search_fields = ('title', 'description')   # Men gosdum
    filterset_fields = ('completed',)

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Yeni görev oluşturulurken owner otomatik olarak giriş yapan kullanıcı olur
        serializer.save(owner=self.request.user)


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data, is_active=True)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)