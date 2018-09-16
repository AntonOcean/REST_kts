from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token

from core import views

# router = DefaultRouter()
# router.register(r'snippets', views.SnippetViewSet)
# router.register(r'users', views.UserViewSet)

# topic_create = TopicViewSet.as_view({
#     'post': 'create'
# })
# topic_list = TopicViewSet.as_view({
#     'get': 'list',
# })


# API endpoints
urlpatterns = [
    path('topic.create/', views.TopicCreate.as_view(), name='topic-create'),
    path('topic.list/', views.TopicList.as_view(), name='topic-list'),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    path('auth.login/', views.LoginView.as_view(), name='auth-login'),

]
