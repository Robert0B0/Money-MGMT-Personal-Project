from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *

from django.db.models import Sum


from .models import *
from .forms import *


#=================| ACCOUNT SETTINGS |=========================================

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='money_users')
            user.groups.add(group)
            moneyUser.objects.create(
                user=user,
                name=username,
                worth=100,
                email=form.cleaned_data.get('email'),
                
            )

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

            #messages.success(request, 'Account was created for ' + username)
            #return redirect('login_page')


    context = {'form': form}

    return render(request, 'MGMT/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect.')

    context = {}

    return render(request, 'MGMT/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def settingsPage(request):
    records = request.user.moneyuser.moneyrecord_set.all()
    goals = request.user.moneyuser.moneygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = request.user.username
    wallet = request.user.moneyuser.worth

    total_out = request.user.moneyuser.moneyrecord_set.filter(category='expenses').filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_in = request.user.moneyuser.moneyrecord_set.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    if total_out is None:
        total_out = 0
    if total_in is None:
        total_in = 0
    
    balance = wallet - total_out + total_in

    moneyuser = request.user.moneyuser
    form = MoneyUserForm(instance=moneyuser)

    if request.method == 'POST':
        form = MoneyUserForm(request.POST, request.FILES, instance=moneyuser)
        if form.is_valid:
            form.save()
    
    
    context = {'form': form, 'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/user_settings.html', context)




#=================| HOME PAGE |=========================================

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def homePage(request):
    records = request.user.moneyuser.moneyrecord_set.all()
    goals = request.user.moneyuser.moneygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = request.user.username
    wallet = request.user.moneyuser.worth

    total_out = request.user.moneyuser.moneyrecord_set.filter(category='expenses').filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_in = request.user.moneyuser.moneyrecord_set.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    if total_out is None:
        total_out = 0
    if total_in is None:
        total_in = 0
    
    balance = wallet - total_out + total_in


    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/home.html', context)

#=================| MONETARY Record |=========================================

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def recordPage(request):
    records = request.user.moneyuser.moneyrecord_set.all()
    goals = request.user.moneyuser.moneygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = request.user.username
    wallet = request.user.moneyuser.worth

    total_out = request.user.moneyuser.moneyrecord_set.filter(category='expenses').filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_in = request.user.moneyuser.moneyrecord_set.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    if total_out is None:
        total_out = 0
    if total_in is None:
        total_in = 0
    
    balance = wallet - total_out + total_in

    total_expenses = request.user.moneyuser.moneyrecord_set.filter(category='expenses').aggregate(Sum('amount'))['amount__sum']
    total_upkeep = request.user.moneyuser.moneyrecord_set.filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_unforeseen = request.user.moneyuser.moneyrecord_set.filter(category='unforeseen').aggregate(Sum('amount'))['amount__sum']

    total_income = request.user.moneyuser.moneyrecord_set.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    total_dividents = request.user.moneyuser.moneyrecord_set.filter(category='dividents').aggregate(Sum('amount'))['amount__sum']
    total_in_other = request.user.moneyuser.moneyrecord_set.filter(category='other').aggregate(Sum('amount'))['amount__sum']

    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance, 
        'total_expenses' : total_expenses, 'total_upkeep': total_upkeep, 'total_unforeseen': total_unforeseen,
        'total_income': total_income, 'total_dividents': total_dividents, 'total_in_other': total_in_other}

    return render(request, 'MGMT/record_page.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def createRecord(request, pk):
    user = request.user.moneyuser
    form = RecordForm(initial={'user': user})
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'MGMT/record_form.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def updateRecord(request, pk):
    act = moneyRecord.objects.get(id=pk)
    form = RecordForm(instance=act)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=act)
        if form.is_valid:
            form.save()
            return redirect('/records/')

    context = {'form': form}

    return render(request, 'MGMT/record_form.html', context) 

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def deleteRecord(request, pk):
    record = moneyRecord.objects.get(id=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('/records/') 
    context ={'record': record}

    return render(request, 'MGMT/record_delete.html', context)



#=================| GOALS |=========================================

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def goalsPage(request):
    records = request.user.moneyuser.moneyrecord_set.all()
    goals = request.user.moneyuser.moneygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = request.user.username
    wallet = request.user.moneyuser.worth

    total_out = request.user.moneyuser.moneyrecord_set.filter(category='expenses').filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_in = request.user.moneyuser.moneyrecord_set.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    if total_out is None:
        total_out = 0
    if total_in is None:
        total_in = 0
    
    balance = wallet - total_out + total_in

    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/goals_page.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def createGoal(request):
    user = request.user.moneyuser
    form = GoalForm(initial={'user': user})
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/goals/')

    context = {'form': form}

    return render(request, 'MGMT/goal_form.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def updateGoal(request, pk):
    goal = moneyGoals.objects.get(id=pk)
    form = GoalForm(instance=goal)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid:
            form.save()
            return redirect('/goals/')

    context = {'form': form}

    return render(request, 'MGMT/goal_form.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def deleteGoal(request, pk):
    goal = moneyGoals.objects.get(id=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('/goals/')
    
    context = {'goal': goal}

    return render(request, 'MGMT/goal_delete.html', context)

#=================| SAVINGS |=========================================

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def savingsPage(request):
    records = request.user.moneyuser.moneyrecord_set.all()
    goals = request.user.moneyuser.moneygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = request.user.username
    wallet = request.user.moneyuser.worth

    total_out = request.user.moneyuser.moneyrecord_set.filter(category='expenses').filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_in = request.user.moneyuser.moneyrecord_set.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    if total_out is None:
        total_out = 0
    if total_in is None:
        total_in = 0
    
    balance = wallet - total_out + total_in
    
    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/savings_page.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def createSaving(request):
    context = {}

    return render(request, 'MGMT/savings_page.html', context)


#=================| GRAPHS |=========================================

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins','money_users'])
def graphPage(request):
    records = request.user.moneyuser.moneyrecord_set.all()
    goals = request.user.moneyuser.moneygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()

    user_name = request.user.username
    wallet = request.user.moneyuser.worth

    total_out = request.user.moneyuser.moneyrecord_set.filter(category='expenses').filter(category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_in = request.user.moneyuser.moneyrecord_set.filter(category='monthly income').aggregate(Sum('amount'))['amount__sum']
    if total_out is None:
        total_out = 0
    if total_in is None:
        total_in = 0
    
    balance = wallet - total_out + total_in
    
    context = {'records': records, 'total_records':total_records, 'goals': goals, 'total_goals': total_goals, 
        'user_name': user_name, 'balance': balance}

    return render(request, 'MGMT/graph.html', context)

#=================| |=========================================