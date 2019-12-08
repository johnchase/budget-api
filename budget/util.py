"""Utitility functions."""


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
