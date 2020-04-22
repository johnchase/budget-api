"""budget URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.urls import path
from budget.views import ListCreateExpenseView, ExpenseDetailView, BudgetView, SummaryView, PerDiemView, SavingsView

urlpatterns = [
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("expenses/", ListCreateExpenseView.as_view(), name="expenses"),
    path("budget/", BudgetView.as_view(), name="budget"),
    path("summary/", SummaryView.as_view(), name="summary"),
    path("perDiem/", PerDiemView.as_view(), name="perDiem"),
    path("saved/", SavingsView.as_view(), name="saved"),
]
