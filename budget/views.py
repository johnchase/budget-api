"""Views module."""
import datetime
import calendar

from rest_framework import generics
from rest_framework.response import Response

from django.db.models import Sum

from budget.models import Expense
from budget.serializers import ExpenseSerializer
from budget.util import get_per_day, calculate_budgets
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
        result = calculate_budgets(self.queryset, today.month, today.year)
        return Response(result)


class SummaryView(generics.RetrieveAPIView):
    """Class for controlling single expense.

    GET summary/
    """

    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Get the summary data for the current month."""
        today = datetime.date.today()
        month = today.month
        year = today.year

        results = (
            self.queryset.filter(date__year=year, date__month=month)
            .values("budget_category")
            .annotate(amount=Sum("amount"))
        )

        data = {result["budget_category"]: result["amount"] for result in results}
        return Response(data)


class PerDiemView(generics.RetrieveAPIView):
    """Class for controlling single expense.

    GET perDiem/
    """

    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Get the summary data for the current month."""
        month = int(request.GET["month"])
        year = int(request.GET["year"])
        total = get_per_day(self.queryset, month, year)

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        num_month_days = calendar.monthrange(year, month)[1]
        per_day = total / num_month_days

        return Response(per_day)


class SavingsView(generics.RetrieveAPIView):
    """Class for controlling single expense.

    GET saved/
    """

    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Get the total amount saved for the year."""
        today = datetime.date.today()
        saved = 0
        for month in range(1, today.month + 1):
            saved += calculate_budgets(self.queryset, month, today.year)["saved"]
        return Response(saved)
