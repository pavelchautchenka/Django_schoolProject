from django.contrib import admin
from django.urls import path, include
from app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from app import services
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include("debug_toolbar.urls")),
    path("", views.home_page, name="home"),
    path("contacts/", views.contacts_views, name="contacts"),
    path("gallery/", views.gallery_views, name="gallery"),
    path('register/student/', views.register_user, {'user_type': 'student'}, name='register_student'),
    path('register/parent/', views.register_user, {'user_type': 'parent'}, name='register_parent'),
    path('register/teacher/', views.register_user, {'user_type': 'teacher'}, name='register_teacher'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('diary/', views.student_diary, name='student_diary'),
    path('diary/exams/', views.schedule_exams, name='schedule_exams'),
    path('diary/homework/', views.home_work_views,name='home_work'),
    path('diary/schedule/', views.schedule_lessons_view,name='schedule_lessons'),
    path('info/', views.info_views, name='info'),


    path('activate/<uid64>/<token>/', services.activate, name='activate'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
