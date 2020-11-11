from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


# Create your models here.


class moneyUser(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, default='Username')
    worth = models.DecimalField(null=False, max_digits=7, decimal_places=2, default=10.00)
    warning_amount = models.DecimalField(null=False, max_digits=7, decimal_places=2, default=10.00)
    email = models.EmailField(max_length=200, null=True, default='mail@mail.mail')
    profile_pic = models.ImageField(default="profile-default.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class moneyGoals(models.Model):
    CATEGORY = (
                ('Small Goal', 'Small Goal'),
                ('Liability Goal', 'Liability Goal'),
                ('Life Goal', 'Life Goal'),
                ('Investment Goal', 'Investment Goal'),
                )

    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, default='Goal')
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Small Goal')
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return str(self.naming)


class completedmoneyGoals(models.Model):
    CATEGORY = (
                ('Small Goal', 'Small Goal'),
                ('Liability Goal', 'Liability Goal'),
                ('Life Goal', 'Life Goal'),
                ('Investment Goal', 'Investment Goal'),
                )

    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, default='Completed-Goal')
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Small Goal')
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return str(self.naming)


class moneyRecord(models.Model):
    CATEGORY = (
                ('Outcome', (
                            ('expenses', 'Expenses'),
                            ('upkeep', 'Upkeep'),
                            ('unforeseen', 'Unforeseen'),
                            )
                ),
                ('Income', (
                            ('monthly income', 'Monthly Income'),
                            ('dividents', 'Dividents'),
                            ('other', 'Other'),
                            )
                ),
            )
    
    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Record")
    category = models.CharField(max_length=200, null=False, choices=CATEGORY, default='Outcome')
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=False, null=True, default=now)

    def __str__(self):
        return '$' + str(self.amount)
    
    # def __str__(self):
    #     return "{}-{}".format(self.naming, self.amount)


class savingsJar(models.Model):

    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Savings-Jar")
    desired_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.naming)


class growthInvestment(models.Model):

    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    naming = models.CharField(max_length=200, null=False, blank=True, default="Invest-Plan")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    current_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    monthly_contribution = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0)
    interest_rate = models.DecimalField(null=False, max_digits=10, decimal_places=2, 
                                        default=0, validators=[MinValueValidator(Decimal(0.1)), MaxValueValidator(Decimal(100))])
    time_length = models.IntegerField(null=False, default=10)

    
    def __str__(self):
        return str(self.naming)






class bugReport(models.Model):
    PAGE = (
        ('HOME', 'HOME'), 
        ('RECORDS', 'RECORDS'),
        ('GOALS', 'GOALS'),
        ('SAVINGS','SAVINGS'),
        ('INVESTMENTS', 'INVESTMENTS'),
        ('CALENDAR', 'CALENDAR'),
        ('GRAPH', 'GRAPH'),
        ('SETTINGS', 'SETTINGS'),
        ('NAVIGATION', 'NAVIGATION'),
        ('ABOUT','ABOUT'),
    )
    
    user = models.ForeignKey(moneyUser, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    page = models.CharField(max_length=200, null=False, choices=PAGE, default='HOME') 
    details = models.CharField(max_length=1000, null=False, blank=True, default="Report")


    def __str__(self):
        return str(self.page)





    