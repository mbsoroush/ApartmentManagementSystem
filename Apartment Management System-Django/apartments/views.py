from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

from .models import House, Payment, Resident, StatusRequest


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
    if request.user.is_staff and not resident:
        return redirect("manager_dashboard")
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
            my_requests=resident.requests.all()[:10],
            status_choices=[c for c in House.Status.choices if c[0] != house.status],
            has_pending=resident.requests.filter(
                status=StatusRequest.Status.PENDING).exists(),
        )
    return render(request, "apartments/dashboard.html", context)


@login_required
@require_POST
def submit_request(request):
    resident = (
        Resident.objects.filter(user=request.user).select_related("house").first()
    )
    if not resident or not resident.house:
        messages.error(request, "You have no house assigned.")
        return redirect("dashboard")

    requested = request.POST.get("requested_status", "")
    note = request.POST.get("note", "").strip()[:300]

    if requested not in House.Status.values:
        messages.error(request, "Please choose a valid status.")
    elif requested == resident.house.status:
        messages.error(request, "Your house already has that status.")
    elif resident.requests.filter(status=StatusRequest.Status.PENDING).exists():
        messages.error(request, "You already have a pending request.")
    else:
        StatusRequest.objects.create(
            resident=resident, requested_status=requested, note=note)
        messages.success(request, "Your request was sent to the manager.")
    return redirect("dashboard")
