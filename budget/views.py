"""Views module."""
import datetime
import calendar

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.conf import settings

from budget.models import Expense
from budget.serializers import ExpenseSerializer
from budget.util import calculate_budgets
from django.http import HttpResponse

from django.views.generic.base import View


class HomePageView(View):
    def dispatch(request, *args, **kwargs):
        return HttpResponse(status=200)


class ListCreateExpenseView(generics.ListCreateAPIView):
    """Class for getting all expenses.

    GET expense/
    POST expense/
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def post(self, request, *args, **kwargs):
        """Post request data."""
        expense = Expense.objects.create(**request.data)
        return Response(data=ExpenseSerializer(expense).data, status=status.HTTP_201_CREATED)


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

    #    permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Retrieve a single expense."""
        today = datetime.date.today()
        per_day = settings.ALLOWANCE

        week_start = today - datetime.timedelta(days=today.weekday())
        day_of_the_week = (today - week_start).days + 1
        week_total = self.queryset.filter(date__gt=week_start).aggregate(total=Coalesce(Sum("amount"), 0))
        week_data = calculate_budgets(week_total["total"], day_of_the_week, 7, per_day)
        month_start = today.replace(day=1)
        num_month_days = calendar.monthrange(today.year, today.month)[1]
        month_total = self.queryset.filter(date__gt=month_start).aggregate(total=Coalesce(Sum("amount"), 0))
        month_data = calculate_budgets(month_total["total"], today.day, num_month_days, per_day)

        year_start = datetime.date(today.year, 1, 1)
        num_year_days = datetime.datetime.now().timetuple().tm_yday
        year_total = self.queryset.filter(date__gt=year_start).aggregate(total=Coalesce(Sum("amount"), 0))
        year_data = calculate_budgets(year_total["total"], today.day, num_year_days, per_day)

        return Response(data={"week": week_data, "month": month_data, "year": year_data})
