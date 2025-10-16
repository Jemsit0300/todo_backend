from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, RegisterViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'register', RegisterViewSet, basename='register')

urlpatterns = router.urls
