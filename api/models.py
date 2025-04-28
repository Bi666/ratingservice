# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Professor(models.Model):
    id = models.CharField(primary_key=True, max_length=10)  # 如JE1
    name = models.CharField(max_length=100)  # 如Professor J. Excellent

    def __str__(self):
        return f"{self.id}, Professor {self.name}"


class Module(models.Model):
    code = models.CharField(primary_key=True, max_length=10)  # 如CD1
    name = models.CharField(max_length=100)  # 如Computing for Dummies

    def __str__(self):
        return f"{self.code} {self.name}"


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()  # 学年的第一年，如2018
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    professors = models.ManyToManyField(Professor)

    class Meta:
        unique_together = ('module', 'year', 'semester')

    def __str__(self):
        return f"{self.module.code} {self.module.name} - {self.year} Semester {self.semester}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'professor', 'module_instance')

    def __str__(self):
        return f"Rating for {self.professor.id} in {self.module_instance} by {self.user.username}: {self.rating}"