# api/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.db.models import Avg
from .models import Professor, Module, ModuleInstance, Rating
from .serializers import UserSerializer, ProfessorSerializer, ModuleSerializer, ModuleInstanceSerializer, \
    RatingSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class ModuleListView(APIView):
    def get(self, request):
        module_instances = ModuleInstance.objects.all()
        result = []

        for instance in module_instances:
            module_data = {
                'code': instance.module.code,
                'name': instance.module.name,
                'year': instance.year,
                'semester': instance.semester,
                'professors': []
            }

            for professor in instance.professors.all():
                module_data['professors'].append({
                    'id': professor.id,
                    'name': professor.name
                })

            result.append(module_data)

        return Response(result, status=status.HTTP_200_OK)


class ProfessorRatingsView(APIView):
    def get(self, request):
        professors = Professor.objects.all()
        result = []

        for professor in professors:
            avg_rating = Rating.objects.filter(professor=professor).aggregate(Avg('rating'))['rating__avg'] or 0
            rounded_rating = round(avg_rating)

            result.append({
                'id': professor.id,
                'name': professor.name,
                'rating': rounded_rating
            })

        return Response(result, status=status.HTTP_200_OK)


class ProfessorModuleRatingView(APIView):
    def get(self, request, professor_id, module_code):
        try:
            professor = Professor.objects.get(id=professor_id)
            module = Module.objects.get(code=module_code)
            module_instances = ModuleInstance.objects.filter(module=module)

            ratings = Rating.objects.filter(
                professor=professor,
                module_instance__in=module_instances
            )

            if ratings.exists():
                avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
                rounded_rating = round(avg_rating)
                return Response({'rating': rounded_rating}, status=status.HTTP_200_OK)
            else:
                return Response({'rating': 0}, status=status.HTTP_200_OK)
        except (Professor.DoesNotExist, Module.DoesNotExist):
            return Response({'error': 'Professor or module not found'}, status=status.HTTP_404_NOT_FOUND)


class RateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professor_id = request.data.get('professor_id')
        module_code = request.data.get('module_code')
        year = request.data.get('year')
        semester = request.data.get('semester')
        rating_value = request.data.get('rating')

        try:
            professor = Professor.objects.get(id=professor_id)
            module = Module.objects.get(code=module_code)
            module_instance = ModuleInstance.objects.get(
                module=module,
                year=year,
                semester=semester
            )

            # 检查教授是否教授此模块实例
            if professor not in module_instance.professors.all():
                return Response(
                    {'error': 'Professor does not teach this module instance'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 创建或更新评分
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                professor=professor,
                module_instance=module_instance,
                defaults={'rating': rating_value}
            )

            return Response({'success': True}, status=status.HTTP_200_OK)
        except (Professor.DoesNotExist, Module.DoesNotExist, ModuleInstance.DoesNotExist):
            return Response(
                {'error': 'Professor, module or module instance not found'},
                status=status.HTTP_404_NOT_FOUND
            )