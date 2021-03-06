from django.urls import include, path

from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# example: router.register(r'users', views.UserViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'poll', views.PollViewSet)
#router.register(r'category_names', views.ListCategories.as_view())
#router.register(r'category_list', views.ListCategoriesView, basename='category-list')

#router_2 = routers.SimpleRouter()
#router_2.register(r'poll_list', views.PollView, basename='result-list')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/', views.test, name='test'),
    path('testcookie/', views.cookie_session),
    path('getcookie/', views.get_cookies),
    # custom API
    path('category_list/', views.CategoriesView.as_view()),
    path('poll_list/', views.PollView.as_view()),
    path('result_list/', views.ResultsView.as_view()),
    path('poll_stats/', views.PollstatsView.as_view()),
    ]