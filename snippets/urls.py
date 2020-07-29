from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from snippets import views


urlpatterns = [
    path('', views.api_root),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlightView.as_view(), name='snippet-highlight'),

    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    # views based on decorator api_view
    path('snippets_fbv/', views.snippet_list, name='snippet-list-fbv'),
    path('snippets_fbv/<int:pk>/', views.snippet_list),
    # views based on APIView
    path('snippets_apiview/', views.SnippetListAPIView.as_view(), name='snippet-list-apiview'),
    path('snippets_apiview/<int:pk>/', views.SnippetDetailAPIView.as_view(), name='snippet-detail-apiview'),
    # views based on Base GenericAPIView with mixins
    path('snippets_generic_mixin_apiview/', views.SnippetListGenericMixinView.as_view(), name='snippet-list-mixin'),
    path('snippets_generic_mixin_apiview/<int:pk>/', views.SnippetDetailGenericMixinView.as_view(), name='snippet-detail-mixin'),
    # views based on generics views
    path('snippets_list_create_apiview/', views.SnippetListCreateView.as_view(), name='snippet-list-generic'),
    path('snippets_retrieve_update_destroy_apiview/<int:pk>/', views.SnippetRetrieveUpdateDestroyView.as_view(), name='snippet-detail-generic'),
]


# views based on viewsets

# Binding ViewSets to URLs explicitly

snippet_list = views.SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_detail = views.SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlight = views.SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = views.UserViewSet.as_view({
    'get': 'list'
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve'   
})


urlpatterns = [
    path('', views.api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
]


urlpatterns = format_suffix_patterns(urlpatterns)


# Using Routers

# doesn't need views.api_root(creates automatically) and format_suffix_patterns
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls))
]
