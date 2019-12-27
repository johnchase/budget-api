"""Views module."""
import datetime
import calendar

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.permissions import IsAuthenticated

from django.db.models.functions import Coalesce
from django.db.models import Sum

from budget.models import Expense
from budget.serializers import ExpenseSerializer
from budget.util import calculate_budgets


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


#    def get(self, request, *args, **kwargs):
#        """Retrieve a single expense."""
#        try:
#            expense = self.queryset.get(pk=kwargs["pk"])
#            return Response(ExpenseSerializer(expense).data)
#        except Expense.DoesNotExist:
#            return Response(
#                    data={
#                        "message": "Expense with id: {} does not exist".format(kwargs["pk"])
#                        },
#                    status=status.HTTP_404_NOT_FOUND
#                    )
#
#    def put(self, request, *args, **kwargs):
#        """Update a single expense."""
#        try:
#            expense = self.queryset.get(pk=kwargs["pk"])
#            serializer = ExpenseSerializer()
#            updated_expense = serializer.update(expense, request.data)
#            return Response(ExpenseSerializer(updated_expense).data)
#        except Expense.DoesNotExist:
#            return Response(
#                    data={
#                        "message": "Expense with id: {} does not exist".format(kwargs["pk"])
#                        },
#                    status=status.HTTP_404_NOT_FOUND
#                    )
#
#    def delete(self, request, *args, **kwargs):
#        """Delete an expense."""
#        try:
#            expense = self.queryset.get(pk=kwargs["pk"])
#            expense.delete()
#            return Response(status=status.HTTP_204_NO_CONTENT)
#        except Expense.DoesNotExist:
#            return Response(
#                    data={
#                        "message": "Expense with id: {} does not exist".format(kwargs["pk"])
#                        },
#                    status=status.HTTP_404_NOT_FOUND
#                    )


class BudgetView(generics.RetrieveAPIView):
    """Class to return budget numbers for the week and month."""

#    permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()

    def get(self, request, *args, **kwargs):
        """Retrieve a single expense."""
        today = datetime.date.today()
        per_day = 68.59

        week_start = today - datetime.timedelta(days=today.weekday())
        day_of_the_week = (today - week_start).days + 1
        week_total = self.queryset.filter(date__gt=week_start).aggregate(total=Coalesce(Sum("amount"), 0))
        week_data = calculate_budgets(week_total["total"], day_of_the_week, 7, per_day)
        month_start = today.replace(day=1)
        num_month_days = calendar.monthrange(today.year, today.month)[1]
        month_total = self.queryset.filter(date__gt=month_start).aggregate(total=Coalesce(Sum("amount"), 0))
        month_data = calculate_budgets(month_total["total"], today.day, num_month_days, per_day)

        return Response(data={"week": week_data, "month": month_data})
