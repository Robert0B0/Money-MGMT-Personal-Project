from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    #path('login/', views.loginPage, name="login"),
    #path('register/', views.registerPage, name="register"),
    path('setting/', views.settingsPage, name="settings"),

    path('', views.homePage, name="home"),
    
    path('records/', views.recordPage, name="record_page"),
    path('record_form/', views.createRecord, name="record_form"),
    path('update_record/<str:pk>/', views.updateRecord, name="update_record"),
    path('delete_record/<str:pk>/', views.deleteRecord, name="delete_record"),

    path('goals/', views.goalsPage, name="goals_page"),
    path('goal_form/', views.createGoal, name="goal_form"),
    path('update_goal/<str:pk>/', views.updateGoal, name="update_goal"),
    path('delete_goal/<str:pk>/', views.deleteGoal, name="delete_goal"),

    path('graph/', views.graphPage, name="graphs"),


]
