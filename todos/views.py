from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Todo
from .serializers import TodoSerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend


# ToDo CRUD API
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = []
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # Men gosdum
    search_fields = ('title', 'description')   # Men gosdum
    filterset_fields = ('completed',)

    def get_queryset(self):
        # Sadece giriş yapan kullanıcının görevlerini getir
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Yeni görev oluşturulurken owner otomatik olarak giriş yapan kullanıcı olur
        serializer.save(owner=self.request.user)


# 🧍‍♂️ Kullanıcı Kayıt (Register)
# @api_view(['POST'])
# def register(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#
#     if username is None or password is None:
#         return Response({'error': 'Username ve password zorunludur.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     if User.objects.filter(username=username).exists():
#         return Response({'error': 'Bu kullanıcı adı zaten alınmış.'}, status=status.HTTP_400_BAD_REQUEST)
#
#     user = User.objects.create_user(username=username, password=password)
#     return Response({'message': 'Kayıt başarılı!'}, status=status.HTTP_201_CREATED)


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)