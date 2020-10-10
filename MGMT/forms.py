from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class ActivityForm(ModelForm):
    class Meta:
        model = moneyActivity
        fields = '__all__'

class GoalForm(ModelForm):
    class Meta:
        model = moneyGoals
        fields = '__all__'

#class createUserForm(UserCreationForm):
#    class Meta:
#        model = moneyUser
#        fields = ['username', 'email', 'password1', 'password2']