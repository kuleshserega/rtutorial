from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
    ListAPIView, RetrieveAPIView
)
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin,
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from snippets.models import Snippet
from snippets.serializers import UserSerializer, SnippetSerializer
from snippets.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class UserList(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetail(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SnippetHighlightView(GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# views based on decorator api_view
# won't work because of changes related with adding user to snippet model (owner)


@api_view(['GET', 'POST'])
def snippet_list(request):
    """Returns list of all code snippets or create new."""
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """Retrieve, update or delete snippet."""
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# views based on APIView
# won't work because of changes related with adding user to snippet model (owner)


class SnippetListAPIView(APIView):

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist as e:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return serializer.data

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# views based on Base GenericAPIView with mixins


class SnippetListGenericMixinView(ListModelMixin,
                                  CreateModelMixin,
                                  GenericAPIView):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # defined in CreateModelMixin
        # it needs to be override because of owner NOT NULL constraint
        serializer.save(owner=self.request.user)


class SnippetDetailGenericMixinView(RetrieveModelMixin,
                                    UpdateModelMixin,
                                    DestroyModelMixin,
                                    GenericAPIView):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# views based on generics views


class SnippetListCreateView(ListCreateAPIView):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# views based on viewsets


class UserViewSet(ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SnippetViewSet(ModelViewSet):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
