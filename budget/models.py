"""Module for model classes."""
from django.db import models


class Expense(models.Model):
    """Expense model class."""

    amount = models.FloatField(null=False)
    date = models.DateTimeField(null=False)
    category = models.CharField(max_length=50, null=False)
    budget_category = models.CharField(max_length=50, null=False)
    business = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    budget_calculation = models.BooleanField(null=True)

    def __str__(self):
        """Represent the model as a string."""
        return "{} - {}".format(self.category, self.amount)

    class Meta:
        """Meta class for ORM."""

        ordering = ["-date"]
