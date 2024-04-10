from django.urls import path
from ..api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('home/', views.NewsListAPIView.as_view(), name='news_list'),
    path('register/student/', views.StudentCreateAPIView.as_view(), name='api_register_student'),
    path('register/parent/', views.ParentCreateAPIView.as_view(), name='api_register_parent'),
    path('register/teacher/', views.TeacherCreateAPIView.as_view(), name='api_register_teacher'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),

    path('student/dashboard/', views.StudentDashboardAPIView.as_view(), name='api_student_dashboard'),
    path('student/exams/', views.StudentScheduleExamsAPIView.as_view(), name='api_student_exams'),
    path('student/homework/', views.StudentHomeWorkAPIView.as_view(), name='api_student_homework'),

    path('parent/dashboard/', views.ParentDashboardAPIView.as_view(), name='api_parent_dashboard'),
    path('parent/messages/', views.ParentMessageAPIView.as_view(), name='api_parent_messages'),
    path('parent/messages/delete/<int:message_id>/',views.DeleteMessageAPIView.as_view(), name='api_delete_message'),
    path('parent/homework/', views.ParentHomeWorkAPIView.as_view(), name='api_parent_homework'),
    path('parent/schedule/', views.ParentScheduleAPIView.as_view(), name='api_parent_schedule'),

    path('teacher/schedule/', views.TeacherDashboardAPIView.as_view(), name='api_teacher_schedule'),


]
