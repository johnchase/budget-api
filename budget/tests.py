"""Test module for all views."""
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.contrib.auth.models import User
from django.urls import reverse

from budget.models import Expense
from budget.serializers import ExpenseSerializer

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

    @staticmethod
    def create_expense(amount="", date="", category="", business=""):
        """Create an expense object for testing."""
        Expense.objects.create(amount=amount, date=date, category=category, business=business)


class GetAllExpensesTest(BaseViewTest):
    """Test class for Expense view."""

    def test_get_all_expenses(self):
        """Ensure that all expensses added in the setUp method exist."""
        self.create_expense(10, "2019-01-01", "item", "Amazon")
        self.create_expense(0.01, "2018-10-26", "gas", "shell")

        response = self.client.get(reverse("expenses"))
        expected = Expense.objects.all()
        serialized = ExpenseSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetBudgetsTest(BaseViewTest):
    """Test class for budget view."""

    @freeze_time("2000-01-05")
    def test_get_budget(self):
        """Ensure that all budget with no expenses is correct."""
        response = self.client.get(reverse("budget"))
        expected = {
            "week": {"total": 0.0, "perDay": 0.0, "leftPerDay": 96.03, "saved": 205.77},
            "month": {"total": 0.0, "perDay": 0.0, "leftPerDay": 78.75, "saved": 342.95}, }
        self.assertEqual(response.data, expected)
