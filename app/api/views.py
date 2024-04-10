from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from hwork.api.permissions import IsOwnerOrReadOnly
from hwork.api.serializers import NoteSerializer, TagSerializer
from hwork.models import Note, Tag


class NoteListAPIView(ListCreateAPIView):
    queryset = Note.objects.all()[:5]
    serializer_class = NoteSerializer


class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'id'
    permission_classes = [IsOwnerOrReadOnly]


class TagListCreateAPIViews(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
