# api/admin.py

from django.contrib import admin
from .models import Professor, Module, ModuleInstance, Rating


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(ModuleInstance)
class ModuleInstanceAdmin(admin.ModelAdmin):
    list_display = ('module', 'year', 'semester', 'get_professors')
    list_filter = ('year', 'semester')
    search_fields = ('module__code', 'module__name')

    def get_professors(self, obj):
        return ", ".join([p.name for p in obj.professors.all()])

    get_professors.short_description = 'Professors'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'professor', 'module_instance', 'rating')
    list_filter = ('rating',)