# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Professor, Module, ModuleInstance, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'name']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['code', 'name']


class ModuleInstanceSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    professors = ProfessorSerializer(many=True)

    class Meta:
        model = ModuleInstance
        fields = ['module', 'year', 'semester', 'professors']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['professor', 'module_instance', 'rating']