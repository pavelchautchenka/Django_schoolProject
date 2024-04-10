from django.contrib import admin
from django.urls import path, include
from app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from app import services
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('__debug__/', include("debug_toolbar.urls")),

                  path("", views.home_page, name="home"),

                  path("contacts/", views.contacts_views, name="contacts"),

                  path("gallery/", views.gallery_views, name="gallery"),

                  path('search/', views.search, name='search_results'),

                  path('register/student/', views.register_user, {'user_type': 'student'}, name='register_student'),
                  path('register/parent/', views.register_user, {'user_type': 'parent'}, name='register_parent'),
                  path('register/teacher/', views.register_user, {'user_type': 'teacher'}, name='register_teacher'),
                  path('login/', views.user_login, name='login'),
                  path('logout/', views.logout_user, name='logout'),

                  path("register/pasword-resetform", views.reset_form_view, name='resetform'),
                  path("password_reset/", views.reset_password_view, name="reset-password"),
                  path("new_password<uidb64>/<token>", views.confirm_new_password_view, name="new-password"),

                  path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),
                  path('parent_message/', views.parent_message, name='parent_message'),
                  path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
                  path('parent_hm/', views.parent_home_work_views, name='parent_hw'),
                  path('parent_schedule/', views.parent_schedule_views, name='parent_schedule'),

                  path('teacher_dashboar/', views.teacher_dashboard, name='teacher_dashboard'),
                  path('teacher_send/', views.teacher_send_message, name='teacher_send_message'),
                  path('teacher_post_grade/', views.teacher_post_grade, name='teacher_post_grade'),
                  path('teacher_post_hw/', views.teacher_create_hw, name='teacher_post_homework'),

                  path('diary/', views.student_dashboard, name='student_diary'),
                  path('diary/exams/', views.student_schedule_exams, name='schedule_exams'),
                  path('diary/homework/', views.student_home_work_views, name='home_work'),
                  path('diary/schedule/', views.student_schedule_lessons_view, name='schedule_lessons'),
                  path('info/', views.info_views, name='info'),

                  path('activate/<uid64>/<token>/', services.activate, name='activate'),

                  path('api/', include('app.api.urls')),

                  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
