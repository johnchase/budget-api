"""Views module."""
import datetime
import calendar

from rest_framework import generics
from rest_framework.response import Response

from django.db.models.functions import Coalesce
from django.db.models import Sum

from budget.models import Expense
from budget.serializers import ExpenseSerializer
from budget.util import calculate_budgets, get_budget_summary, get_expenses
from django.http import HttpResponse

from django.views.generic.base import View


class HomePageView(View):
    """Class for aws eb health check."""

    def dispatch(request, *args, **kwargs):
        """Provide generic endpoint that returns 200 for health checker."""
        return HttpResponse(status=200)


class ListCreateExpenseView(generics.ListCreateAPIView):
    """Class for getting all expenses.

    GET expenses/
    POST expenses/
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Class for controlling single expense.

    GET expense/:id/
    PUT expense/:id/
    DELETE expense/:id/
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = "pk"


class BudgetView(generics.RetrieveAPIView):
    """Class to return budget numbers for the week and month."""

    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Retrieve a single expense."""
        today = datetime.date.today()
        month = today.month
        year = today.year
        # Per day for the current month is based on the expenditures from the previous month
        if month == 12:
            month = 1
        else:
            month -= 1

        per_day = 14

        num_month_days = calendar.monthrange(year, today.month)[1]
        per_day = get_expenses(self.queryset, month, year) / num_month_days

        month_start = today.replace(day=1)
        month_total = self.queryset.filter(date__gt=month_start).aggregate(total=Coalesce(Sum("amount"), 0))
        month_data = calculate_budgets(month_total["total"], today.day, num_month_days, per_day)

        return Response(data=month_data)


class SummaryView(generics.RetrieveAPIView):
    """Class for controlling single expense.

    GET summary/
    """

    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Get the summary data for the current month."""
        result = get_budget_summary(self.queryset)

        return Response(result)


class PerDiemView(generics.RetrieveAPIView):
    """Class for controlling single expense.

    GET perDiem/
    """

    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Get the summary data for the current month."""
        month = datetime.datetime.today().month
        year = datetime.datetime.today().year

        days_next_month = calendar.monthrange(year, month)[1]
        daily = get_expenses(self.queryset)
        daily = daily / days_next_month
        return Response(round(daily, 2))


class SavingsView(generics.RetrieveAPIView):
    """Class for controlling single expense.

    GET saved/
    """

    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Get the total amount saved for the year."""
        result = get_expenses(self.queryset, budget_calculation=True, expense_calculation=True, month=False)
        return Response(result)
