"""Serializers for budget app."""
from budget.models import Expense
from rest_framework import serializers


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense Model."""

    class Meta:
        """Meta class defining meta data."""

        model = Expense
        fields = "__all__"
