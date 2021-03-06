from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class MoneyUserForm(ModelForm):
    class Meta:
        model = moneyUser
        fields = '__all__'
        exclude = ['user']

class RecordForm(ModelForm):
    class Meta:
        model = moneyRecord
        fields = '__all__'
        #fields = ['naming', 'category', 'amount']

class GoalForm(ModelForm):
    class Meta:
        model = moneyGoals
        fields = '__all__'
        #fields = ['naming', 'category', 'amount', 'due_date']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SavingsForm(ModelForm):
    class Meta:
        model = savingsJar
        fields = '__all__'
