from django.urls import include, path

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# example: router.register(r'users', views.UserViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'poll', views.PollViewSet)
#router.register(r'category_names', views.ListCategories.as_view())

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/', views.test, name='test'),
    ]