"""Test module for all views."""
import datetime
import pytz

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.contrib.auth.models import User
from django.urls import reverse

from django.conf import settings

from budget.models import Expense
from budget.serializers import ExpenseSerializer
from budget.util import get_per_day

from freezegun import freeze_time


class BaseViewTest(APITestCase):
    """Base class test for test classes."""

    client = APIClient()

    def setUp(self):
        """Test setup."""
        self.user = User.objects.create_superuser(
            username="test_user", email="test@mail.com", password="testing", first_name="test", last_name="user"
        )

        self.client.login(username="test_user", password="testing")


class TestUtil(BaseViewTest):
    """Test class for Util functions."""

    def test_get_daily(self):
        """Ensure that all expensses added in the setUp method exist."""
        Expense.objects.create(
            amount=300,
            date=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC),
            budget_category="Income",
            category="Paycheck",
            budget_calculation=True,
        )
        queryset = Expense.objects.all()
        result = get_per_day(queryset=queryset, month=8, year=2011)
        expected = 10
        self.assertEqual(result, expected)


# class TestListCreateExpenseView(BaseViewTest):
#    """Test class for Expense view."""
#
#    def test_get_all_expenses(self):
#        """Ensure that all expensses added in the setUp method exist."""
#        Expense.objects.create(
#            amount=10,
#            date=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC),
#            category="item",
#            expense_calculation=True,
#        )
#        Expense.objects.create(
#            amount=0.01,
#            date=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC),
#            category="item",
#            expense_calculation=True,
#        )
#
#        response = self.client.get(reverse("expenses"), secure=True)
#        expected = Expense.objects.all()
#        serialized = ExpenseSerializer(expected, many=True)
#        self.assertEqual(response.data["results"], serialized.data)
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#    def test_post_expense_view(self):
#        """Test that post an expense works as expected."""
#        data = {
#            "date": "2018-03-12T19:00:00",
#            "amount": 50,
#            "category": "Restaurants",
#            "budget_category": "Expenses",
#            "business": "",
#            "description": "",
#            "expense_calculation": "true",
#            "budget_calculation": "",
#        }
#        url = "/expenses/"
#
#        response = self.client.post(url, data, format="json")
#        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#        self.assertEqual(response.data["budget_category"], "Expenses")
#
#
# class GetBudgetsTest(BaseViewTest):
#    """Test class for budget view."""
#
#    @freeze_time("2020-01-20")
#    def test_get_budget(self):
#        """Ensure that all budget with no expenses is correct."""
#        Expense.objects.create(
#            amount=3100,
#            date=datetime.datetime(2019, 12, 15, 8, 15, 12, 0, pytz.UTC),
#            category="Paycheck",
#            budget_category="Income",
#        )
#        Expense.objects.create(
#            amount=710,
#            date=datetime.datetime(2020, 1, 1, 8, 15, 12, 0, pytz.UTC),
#            category="Items",
#            budget_category="Expense",
#        )
#        response = self.client.get(reverse("budget"), secure=True)
#        expected = {"total": 710, "perDay": 35.5, "leftPerDay": 199.17, "saved": 1290}
#
#        self.assertEqual(response.data, expected)
#

#    @freeze_time("2020-01-01")
#    def test_get_budget_1(self):
#        """Ensure that all budget with no expenses is correct."""
#        response = self.client.get(reverse("budget"), secure=True)
#        expected = {"total": 0.0, "perDay": 0.0, "leftPerDay": settings.ALLOWANCE, "saved": settings.ALLOWANCE}
#
#        self.assertEqual(response.data, expected)
#
#    @freeze_time("2020-02-03")
#    def test_get_budget_2(self):
#        """Ensure that budgets in February are correct."""
#        Expense.objects.create(amount=1000, date="2020-01-02", category="item", expense_calculation=True)
#        response = self.client.get(reverse("budget"), secure=True)
#        expected = {
#            "total": 0.0,
#            "perDay": 0.0,
#            "leftPerDay": 69.33,
#            "saved": 193.65,
#        }
#        print(response.data)
#        print(expected)
#        self.assertEqual(response.data, expected)
