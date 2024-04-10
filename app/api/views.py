from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView, DestroyAPIView
from app.models import News, Student, Parent, Teacher, Exam, HomeWork, Lessons, Message
from .serializers import NewsSerializer, StudentSerializer, ParentSerializer, TeacherSerializer, LoginSerializer, \
    ExamSerializer, HomeWorkSerializer, LessonSerializer,MessageSerializer


class NewsListAPIView(ListAPIView):
    queryset = News.objects.all()[:10]
    serializer_class = NewsSerializer


class StudentCreateAPIView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ParentCreateAPIView(CreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


class TeacherCreateAPIView(CreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['username'],
                                password=serializer.validated_data['password'])
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDashboardAPIView(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_object(self):
        if not self.request.user.is_authenticated:
            raise AuthenticationFailed('Пользователь не аутентифицирован')

        try:

            return self.queryset.get(user=self.request.user)
        except Student.DoesNotExist:
            raise NotFound('Студент не найден')


class StudentScheduleExamsAPIView(ListAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Студент не найден')

        try:
            student = Student.objects.only('school_group').get(user=user)
            return Exam.objects.filter(school_group=student.school_group)
        except Student.DoesNotExist:
            raise NotFound('Студент не найден')


class StudentHomeWorkAPIView(ListAPIView):
    serializer_class = HomeWorkSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Студент не найден')

        try:
            student = Student.objects.select_related('school_group').get(user=user)
            current_date = timezone.now()
            return HomeWork.objects.filter(
                group=student.school_group,
                date_deadline__gte=current_date
            )
        except Student.DoesNotExist:
            raise NotFound('Студент не найден')


class StudentScheduleLessonsAPIView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Студент не найден')

        try:
            student = Student.objects.select_related('school_group').get(user=user)
            return Lessons.objects.filter(group=student.school_group)
        except Student.DoesNotExist:
            raise NotFound('Студент не найден')


class ParentDashboardAPIView(RetrieveAPIView):
    serializer_class = ParentSerializer

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Родитель не найден')

        try:
            parent = Parent.objects.get(user=user)
            parent.student = Student.objects.get(parent=parent)
            return parent
        except Parent.DoesNotExist:
            raise NotFound('Родитель не найден')


class ParentMessageAPIView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Родитель не найден')

        try:
            parent = Parent.objects.select_related('user').get(user=user)
            return Message.objects.filter(parent=parent)
        except Parent.DoesNotExist:
            raise NotFound('Родитель не найден')


class DeleteMessageAPIView(DestroyAPIView):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            # Проверка, принадлежит ли сообщение пользователю
            message = Message.objects.get(id=self.kwargs['message_id'], parent__user=self.request.user)
            return message
        except Message.DoesNotExist:
            raise NotFound('Сообщение не найдено')


class ParentHomeWorkAPIView(ListAPIView):
    serializer_class = HomeWorkSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Родитель не найден')

        try:
            parent = Parent.objects.select_related('user').get(user=user)
            student = Student.objects.filter(parent=parent).prefetch_related('school_group').first()
            current_date = timezone.now()
            return HomeWork.objects.filter(group=student.school_group, date_deadline__gte=current_date)
        except (Parent.DoesNotExist, Student.DoesNotExist):
            raise NotFound('Родитель или студент не найден')



class ParentScheduleAPIView(ListAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Родитель не найден')

        try:
            parent = Parent.objects.select_related('user').get(user=user)
            student = Student.objects.filter(parent=parent).prefetch_related('school_group').first()
            current_date = timezone.now()
            return Exam.objects.filter(date__gte=current_date, school_group=student.school_group)
        except (Parent.DoesNotExist, Student.DoesNotExist):
            raise NotFound('Родитель или студент не найден')


class TeacherDashboardAPIView(ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotFound('Учитель не найден')

        try:
            teacher = Teacher.objects.select_related("user").get(user=user)
            current_date = timezone.now()
            end_date = current_date + timedelta(days=7)
            return Lessons.objects.filter(subject=teacher.my_subject, date__gte=current_date, date__lte=end_date)
        except Teacher.DoesNotExist:
            raise NotFound('Учитель не найден')