"""Utitility functions."""
from datetime import datetime
import calendar

from django.db.models import Sum
from django.db.models import Q


def calculate_budgets(amount_spent, current_day, total_days, budget_per_day):
    """Calculate budget statistics.

    Parameters
    ----------
    amount_spent: float
        The total amount that has been spent so far
    current_day: int
        The day number of the week or month. Monday is 1, the 3rd of the month is 3
    total_days: int
        The number of days for which to calculate stats. If calculating for a week it would be 7, if calculating for a
        month it could be 28, 29, 30 or 31
    budget: float
        The budget for a single day

    """
    budget = total_days * budget_per_day
    spent_per_day = round(amount_spent / current_day, 2)
    left_per_day = round((budget - amount_spent) / (total_days + 1 - current_day), 2)
    saved = round((current_day * budget_per_day) - amount_spent, 2)

    return {"total": amount_spent, "perDay": spent_per_day, "leftPerDay": left_per_day, "saved": saved}


def get_per_day(queryset, month, year):
    """Get the grouped summmed values for the budget_category.

    Parameters
    ----------
    queryset: queryset
        The queryset returned from the expense model

    """
    kwargs = {"date__year": year, "date__month": month, "budget_calculation": True}

    print(queryset.values())
    results = (
        queryset.filter(**kwargs)
        .exclude(budget_category="Expense")
        .values("budget_category")
        .annotate(total=Sum("amount"))
        .order_by()
    )

    income = 0
    expenses = 0
    # This for loop gets around the issue where there may not be a value in the database for a given category
    for result in results:
        if result["budget_category"] == "Income":
            income += result["total"]
        else:
            expenses += result["total"]
    print(income, "********************")
    total = income - expenses
    if month == 12:
        month = 0
    num_month_days = calendar.monthrange(year, month + 1)[1]

    return total / num_month_days


def get_budget_summary(queryset, month=True):
    """Get the grouped summmed values for the budget_category.

    Parameters
    ----------
    queryset: queryset
        The queryset returned from the expense model

    """
    kwargs = {"date__year": datetime.today().year}

    if month:
        kwargs["date__month"] = datetime.today().month

    results = queryset.filter(**kwargs).values("budget_category").annotate(total=Sum("amount")).order_by()
    data = {}
    for result in results:
        data[result["budget_category"]] = result["total"]

    return data


def get_expenses(queryset, budget_calculation=False, expense_calculation=True, month=True):
    """Get the daily expense for a given month.

    Parameters
    ----------
    queryset: queryset
        The queryset returned from the expense model
    month: int
        The number of the month to retrieve
    year: int
        The year to retrieve data for

    """
    if budget_calculation and expense_calculation:
        queryset = queryset.filter(Q(budget_calculation=True) | Q(expense_calculation=True))
    else:
        queryset = queryset.filter(budget_calculation=budget_calculation, expense_calculation=expense_calculation)

    results = get_budget_summary(queryset, month)

    income = 0
    expenses = 0
    # This for loop gets around the issue where there may not be a value in the database for a given category
    for key, value in results.items():
        if key == "Income":
            income += value
        else:
            expenses += value

    return income - expenses
