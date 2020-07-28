from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views


urlpatterns = [
    path('', views.api_root),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlightView.as_view()),

    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    # views based on decorator api_view
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_list),
    # views based on APIView
    path('snippets_apiview/', views.SnippetListView.as_view()),
    path('snippets_apiview/<int:pk>/', views.SnippetDetailView.as_view()),
    # views based on Base GenericAPIView with mixins
    path('snippets_generic_mixin_apiview/', views.SnippetListGenericMixinView.as_view(), name='snippet-list'),
    path('snippets_generic_mixin_apiview/<int:pk>/', views.SnippetDetailGenericMixinView.as_view()),
    # views based on generics views
    path('snippets_list_create_apiview/', views.SnippetListGenericMixinView.as_view()),
    path('snippets_retrieve_update_destroy_apiview/<int:pk>/', views.SnippetDetailGenericMixinView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
