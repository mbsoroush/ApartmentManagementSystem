from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils.dateparse import parse_date

from .models import Payment, Resident


def _parse_date(value):
    try:
        return parse_date(value) if value else None
    except ValueError:
        return None


@login_required
def dashboard(request):
    resident = (
        Resident.objects.filter(user=request.user).select_related("house").first()
    )
    house = resident.house if resident else None

    context = {"house": house}
    if house:
        payments = Payment.objects.filter(house=house)

        debts = payments.filter(paid_date__isnull=True).order_by("due_date")
        total_debt = debts.aggregate(total=Sum("amount"))["total"] or 0

        reason = request.GET.get("reason", "")
        date_from = request.GET.get("date_from", "")
        date_to = request.GET.get("date_to", "")

        history = payments
        if reason in Payment.Reason.values:
            history = history.filter(reason=reason)
        else:
            reason = ""
        if _parse_date(date_from):
            history = history.filter(due_date__gte=_parse_date(date_from))
        if _parse_date(date_to):
            history = history.filter(due_date__lte=_parse_date(date_to))

        context.update(
            debts=debts,
            total_debt=total_debt,
            history=history.order_by("-due_date"),
            reasons=Payment.Reason.choices,
            reason=reason,
            date_from=date_from,
            date_to=date_to,
        )
    return render(request, "apartments/dashboard.html", context)
