# api/urls.py

from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    ModuleListView, ProfessorRatingsView,
    ProfessorModuleRatingView, RateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('modules/', ModuleListView.as_view(), name='module-list'),
    path('professors/ratings/', ProfessorRatingsView.as_view(), name='professor-ratings'),
    path('professors/<str:professor_id>/modules/<str:module_code>/rating/',
         ProfessorModuleRatingView.as_view(), name='professor-module-rating'),
    path('rate/', RateView.as_view(), name='rate'),
]