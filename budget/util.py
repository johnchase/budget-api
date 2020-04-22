"""Utitility functions."""
import datetime
import calendar
from django.db.models import Sum


def calculate_budgets(queryset, month, year):
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
    if month == 1:
        budget_month = 12
        budget_year = year - 1
    else:
        budget_month = month - 1
        budget_year = year

    budget = get_per_day(queryset, budget_month, budget_year)
    num_month_days = calendar.monthrange(year, month)[1]
    per_day = budget / num_month_days

    spent = queryset.filter(date__year=year, date__month=month, budget_category="Purchase").aggregate(Sum("amount"))[
        "amount__sum"
    ]
    if not spent:
        spent = 0.0

    today = datetime.date.today()
    if today.month == month:
        current_day = today.day
    else:
        current_day = num_month_days

    spent_per_day = round(spent / current_day, 2)
    left_per_day = round((budget - spent) / (num_month_days + 1 - current_day), 2)
    saved = round((current_day * per_day) - spent, 2)
    return {"total": spent, "perDay": spent_per_day, "leftPerDay": left_per_day, "saved": saved}


def get_per_day(queryset, month, year):
    """Get the grouped summmed values for the budget_category.

    Parameters
    ----------
    queryset: queryset
        The queryset returned from the expense model

    """
    results = (
        queryset.filter(date__year=year, date__month=month, budget_calculation=True)
        .exclude(budget_category="Purchase")
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
    total = income - expenses

    return total
