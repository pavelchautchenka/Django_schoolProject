from django.urls import path
from .views import NoteListAPIView, NoteDetailAPIView, TagListCreateAPIViews

#/api/posts/
app_name = 'posts:api'

urlpatterns = [
    # другие маршруты
    path('notes/', NoteListAPIView.as_view(), name='notes'),
    path('notes/<id>/', NoteDetailAPIView.as_view(), name='note-detail'),
    path('tags/', TagListCreateAPIViews.as_view(), name='tags'),

]