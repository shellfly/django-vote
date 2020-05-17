from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('comments/', views.comments),
    path('api/', include(router.urls)),
]
