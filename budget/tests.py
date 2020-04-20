"""Test module for all views."""
import datetime
import pytz

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.contrib.auth.models import User
from django.urls import reverse

from budget.models import Expense
from budget.serializers import ExpenseSerializer
from budget.util import get_per_day, calculate_budgets

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
        expected = 300
        self.assertEqual(result, expected)

    @freeze_time("2020-03-20")
    def test_calculate_budgets(self):
        """Check that calculate budgets does what it should."""
        Expense.objects.create(
            amount=3100,
            date=datetime.datetime(2019, 12, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )
        Expense.objects.create(
            amount=2900,
            date=datetime.datetime(2020, 1, 27, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )

        Expense.objects.create(
            amount=1000,
            date=datetime.datetime(2020, 2, 10, 8, 15, 12, 0, pytz.UTC),
            category="Item",
            budget_category="Purchase",
        )
        queryset = Expense.objects.all()
        result = calculate_budgets(queryset, month=1, year=2020)
        expected = 3100
        self.assertEqual(result["saved"], expected)


class TestListCreateExpenseView(BaseViewTest):
    """Test class for Expense view."""

    def test_get_all_expenses(self):
        """Ensure that all expensses added in the setUp method exist."""
        Expense.objects.create(
            amount=10, date=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC), category="item",
        )
        Expense.objects.create(
            amount=0.01, date=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC), category="item",
        )

        response = self.client.get(reverse("expenses"), secure=True)
        expected = Expense.objects.all()
        serialized = ExpenseSerializer(expected, many=True)
        self.assertEqual(response.data["results"], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_expense_view(self):
        """Test that post an expense works as expected."""
        data = {
            "date": "2018-03-12T19:00:00",
            "amount": 50,
            "category": "Restaurants",
            "budget_category": "Expenses",
            "business": "",
            "description": "",
            "budget_calculation": "",
        }
        url = "/expenses/"

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["budget_category"], "Expenses")


class TestPerDiem(BaseViewTest):
    """Test class for perDiem endpoint."""

    def test_get_per_diem(self):
        """Ensure that all expensses added in the setUp method exist."""
        Expense.objects.create(
            amount=1000,
            date=datetime.datetime(2011, 8, 30, 8, 15, 12, 0, pytz.UTC),
            budget_category="Income",
            category="item",
            budget_calculation=True,
        )
        Expense.objects.create(
            amount=400,
            date=datetime.datetime(2011, 8, 1, 8, 15, 12, 0, pytz.UTC),
            category="item",
            budget_category="Savings",
            budget_calculation=True,
        )

        response = self.client.get("/perDiem/?month=8&year=2011", secure=True)
        self.assertEqual(response.data, 20)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetBudgetsTest(BaseViewTest):
    """Test class for budget view."""

    @freeze_time("2020-01-20")
    def test_get_budget(self):
        """Ensure that all budget with no expenses is correct."""
        Expense.objects.create(
            amount=3100,
            date=datetime.datetime(2019, 12, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )
        Expense.objects.create(
            amount=710,
            date=datetime.datetime(2020, 1, 1, 8, 15, 12, 0, pytz.UTC),
            category="Items",
            budget_category="Purchase",
        )
        response = self.client.get(reverse("budget"), secure=True)
        expected = {"total": 710.0, "perDay": 35.5, "leftPerDay": 199.17, "saved": 1290.0}

        self.assertEqual(response.data, expected)

    @freeze_time("2019-06-20")
    def test_get_budget_1(self):
        """Ensure that all budget with no expenses is correct."""
        Expense.objects.create(
            amount=3000,
            date=datetime.datetime(2019, 5, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )
        response = self.client.get(reverse("budget"), secure=True)
        expected = {"total": 0.0, "perDay": 0.0, "leftPerDay": 272.73, "saved": 2000.0}

        self.assertEqual(response.data, expected)

    @freeze_time("2020-04-11")
    def test_get_budget_2(self):
        """Ensure that all budget with no expenses is correct."""
        Expense.objects.create(
            amount=3000,
            date=datetime.datetime(2020, 3, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )

        Expense.objects.create(
            amount=1000,
            date=datetime.datetime(2020, 4, 11, 8, 15, 12, 0, pytz.UTC),
            category="Items",
            budget_category="Purchase",
        )
        response = self.client.get(reverse("budget"), secure=True)
        expected = {"total": 1000.0, "perDay": 90.91, "leftPerDay": 100.0, "saved": 100.0}

        self.assertEqual(response.data, expected)


class TestSummaryView(BaseViewTest):
    """Test class for summary endpoints."""

    @freeze_time("2020-04-11")
    def test_get_summary(self):
        """Ensure that summary is correct."""
        Expense.objects.create(
            amount=3000,
            date=datetime.datetime(2020, 4, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )

        Expense.objects.create(
            amount=1000,
            date=datetime.datetime(2020, 4, 11, 8, 15, 12, 0, pytz.UTC),
            category="Items",
            budget_category="Purchase",
        )
        response = self.client.get(reverse("summary"), secure=True)
        expected = {"Income": 3000, "Purchase": 1000}

        self.assertEqual(response.data, expected)


class TestSavingsView(BaseViewTest):
    """Test class for savings endpoint."""

    @freeze_time("2020-01-10")
    def test_get_saved(self):
        """Ensure that saved is correct."""
        Expense.objects.create(
            amount=3100,
            date=datetime.datetime(2019, 12, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )
        response = self.client.get(reverse("saved"), secure=True)
        expected = 1000

        self.assertEqual(response.data, expected)

    @freeze_time("2020-02-11")
    def test_get_saved_2(self):
        """Ensure that summary is correct."""
        Expense.objects.create(
            amount=3100,
            date=datetime.datetime(2019, 12, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )
        Expense.objects.create(
            amount=2900,
            date=datetime.datetime(2020, 1, 27, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )

        Expense.objects.create(
            amount=1000,
            date=datetime.datetime(2020, 2, 10, 8, 15, 12, 0, pytz.UTC),
            category="Item",
            budget_category="Purchase",
        )
        response = self.client.get(reverse("saved"), secure=True)
        expected = 3200

        self.assertEqual(response.data, expected)

    @freeze_time("2020-01-01")
    def test_get_saved_3(self):
        """Ensure that summary is correct."""
        Expense.objects.create(
            amount=3100,
            date=datetime.datetime(2019, 12, 15, 8, 15, 12, 0, pytz.UTC),
            category="Paycheck",
            budget_category="Income",
            budget_calculation=True,
        )
        response = self.client.get(reverse("saved"), secure=True)
        expected = 100

        self.assertEqual(response.data, expected)
