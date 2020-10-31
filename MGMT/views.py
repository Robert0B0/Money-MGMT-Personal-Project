from django.shortcuts import render, redirect
# from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user
from .decorators import allowed_users

from django.db.models import Sum

from .models import moneyGoals, moneyRecord, moneyUser, savingsJar, completedmoneyGoals
from .forms import RecordForm, GoalForm, CreateUserForm, SavingsForm
from .forms import MoneyUserForm

from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime


# ACCOUNT-SETTINGS #
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
            # messages.success(request, 'Account was created for ' + username)
            # return redirect('login_page')
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
@allowed_users(allowed_roles=['admins', 'money_users'])
def settingsPage(request):
    moneyuser = request.user.moneyuser
    form = MoneyUserForm(instance=moneyuser)
    if request.method == 'POST':
        form = MoneyUserForm(request.POST, request.FILES, instance=moneyuser)
        if form.is_valid:
            form.save()
    ctx = {'form': form}
    context = {**context_add(request), **ctx}
    return render(request, 'MGMT/user_settings.html', context)


# Global #
def context_add(request):
    records = request.user.moneyuser.moneyrecord_set.all()
    goals = request.user.moneyuser.moneygoals_set.all()
    total_records = records.count()
    total_goals = goals.count()
    user_name = request.user.username
    warning = request.user.moneyuser.warning_amount
    wallet = request.user.moneyuser.worth

    total_expenses = request.user.moneyuser.moneyrecord_set.filter(
        Q(category='expenses') | 
        Q(category='upkeep') | 
        Q(category='unforeseen')
    ).aggregate(Sum('amount'))['amount__sum']

    total_income = request.user.moneyuser.moneyrecord_set.filter(
        Q(category='monthly income') | 
        Q(category='dividents') | 
        Q(category='other')
    ).aggregate(Sum('amount'))['amount__sum']

    if total_expenses is None:
        total_expenses = 0
    if total_income is None:
        total_income = 0

    balance = wallet - total_expenses + total_income
    context = {
        'records': records, 'total_records': total_records,
        'goals': goals, 'total_goals': total_goals, 'user_name': user_name,
        'balance': balance, 'warning': warning}

    return context


# HOME PAGE #
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def homePage(request):
    context = context_add(request)
    return render(request, 'MGMT/home.html', context)


# MONETARY Record #
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def recordPage(request):
    total_expenses = request.user.moneyuser.moneyrecord_set.filter(
        category='expenses').aggregate(Sum('amount'))['amount__sum']
    total_upkeep = request.user.moneyuser.moneyrecord_set.filter(
        category='upkeep').aggregate(Sum('amount'))['amount__sum']
    total_unforeseen = request.user.moneyuser.moneyrecord_set.filter(
        category='unforeseen').aggregate(Sum('amount'))['amount__sum']
    total_income = request.user.moneyuser.moneyrecord_set.filter(
        category='monthly income').aggregate(Sum('amount'))['amount__sum']
    total_dividents = request.user.moneyuser.moneyrecord_set.filter(
        category='dividents').aggregate(Sum('amount'))['amount__sum']
    total_in_other = request.user.moneyuser.moneyrecord_set.filter(
        category='other').aggregate(Sum('amount'))['amount__sum']

    if total_expenses is None:
        total_expenses = 0
    if total_upkeep is None:
        total_upkeep = 0
    if total_unforeseen is None:
        total_unforeseen = 0
    if total_income is None:
        total_income = 0
    if total_dividents is None:
        total_dividents = 0
    if total_in_other is None:
        total_in_other = 0

    ctx = {
        'total_expenses': total_expenses, 'total_upkeep': total_upkeep,
        'total_unforeseen': total_unforeseen, 'total_income': total_income,
        'total_dividents': total_dividents, 'total_in_other': total_in_other}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/record_page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def createRecord(request):
    user = request.user.moneyuser
    form = RecordForm(initial={'user': user})
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/records/')
    ctx = {'form': form}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/record_create.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def updateRecord(request, pk):
    record = moneyRecord.objects.get(id=pk)
    form = RecordForm(instance=record)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid:
            form.save()
            return redirect('/records/')
    ctx = {'form': form, 'record': record}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/record_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def deleteRecord(request, pk):
    record = moneyRecord.objects.get(id=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('/records/')
    ctx = {'record': record}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/record_delete.html', context)


# GOALS #
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def goalsPage(request):
    comp_goals = request.user.moneyuser.completedmoneygoals_set.all()
    total_comp = comp_goals.count()
    ctx = {'comp_goals': comp_goals, 'total_comp': total_comp}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/goals_page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def createGoal(request):
    user = request.user.moneyuser
    form = GoalForm(initial={'user': user})
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/goals/')

    ctx = {'form': form}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/goal_create.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def updateGoal(request, pk):
    goal = moneyGoals.objects.get(id=pk)
    form = GoalForm(instance=goal)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid:
            form.save()
            return redirect('/goals/')
    ctx = {'form': form, 'goal': goal}
    context = {**context_add(request), **ctx}
    return render(request, 'MGMT/goal_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def completeGoal(request, pk):
    goal = moneyGoals.objects.get(id=pk)
    user = request.user.moneyuser
    worth = request.user.moneyuser.worth
    if request.method == 'POST':
        user.worth = worth - goal.amount
        user.save()
        comp_goal = completedmoneyGoals(
                    user=goal.user,
                    naming=goal.naming,
                    category=goal.category,
                    amount=goal.amount,
                    date_created=goal.date_created,
                    due_date=datetime.today(),
        )
        comp_goal.save() 
        goal.delete()
        return redirect('/goals/')

    ctx = {'goal': goal}
    context = {**context_add(request), **ctx}
    return render(request, 'MGMT/goal_complete.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def deleteGoal(request, pk):
    goal = moneyGoals.objects.get(id=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('/goals/')
    ctx = {'goal': goal}
    context = {**context_add(request), **ctx}
    return render(request, 'MGMT/goal_delete.html', context)


# SAVINGS #
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def savingsPage(request):
    jars = request.user.moneyuser.savingsjar_set.all()
    ctx = {'jars': jars}
    context = {**context_add(request), **ctx}
    return render(request, 'MGMT/savings_page.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def createSaving(request):
    user = request.user.moneyuser
    form = SavingsForm(initial={'user': user})
    if request.method == 'POST':
        form = SavingsForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/savings/')
            
    ctx = {'form': form}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/savings_create.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def updateSaving(request, pk):
    jar = savingsJar.objects.get(id=pk)
    form = SavingsForm(instance=jar)
    if request.method == 'POST':
        form = SavingsForm(request.POST, instance=jar)
        if form.is_valid:
            form.save()
            return redirect('/savings/')

    ctx = {'form': form, 'jar': jar}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/savings_form.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def deleteSaving(request, pk):
    jar = savingsJar.objects.get(id=pk)
    if request.method == 'POST':
        jar.delete()
        return redirect('/savings/')

    ctx = {'jar': jar}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/savings_delete.html', context)


@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def breakSaving(request, pk):
    jar = savingsJar.objects.get(id=pk)
    user = request.user.moneyuser
    worth = request.user.moneyuser.worth
    if request.method == 'POST':
        user.worth = worth + jar.amount
        user.save()
        jar.delete()
        return redirect('/savings/')

    ctx = {'jar': jar}
    context = {**context_add(request), **ctx}

    return render(request, 'MGMT/savings_break.html', context)


# GRAPHS #
@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admins', 'money_users'])
def graphPage(request):
    ctx = {}
    context = {**context_add(request), **ctx}
    return render(request, 'MGMT/graph.html', context)


def expenseData(request):
    expenses_data = []
    expenses = request.user.moneyuser.moneyrecord_set.all().filter(
        Q(category='expenses') | Q(category='upkeep') | 
        Q(category='unforeseen')
    ).order_by('date')

    for i in expenses:
        expenses_data.append({i.date.strftime('%m/%d/%Y'): float(i.amount)})

    return JsonResponse(expenses_data, safe=False)


def incomeData(request):
    income_data = []
    incomes = request.user.moneyuser.moneyrecord_set.all().filter(
        Q(category='monthly income') | Q(category='dividents') |
        Q(category='other')    
    ).order_by('date')
    
    for i in incomes:
        income_data.append({(i.date.strftime('%m/%d/%Y') + ' ' + i.naming): float(i.amount)})

    return JsonResponse(income_data, safe=False)


# Other #
def aboutPage(request):
    context = {}
    return render(request, 'MGMT/about.html', context)