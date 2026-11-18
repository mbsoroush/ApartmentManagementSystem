from functools import wraps

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import House, Payment


def staff_required(view):
    """Only logged-in staff (managers) may open the page; everyone else gets 403."""
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["house", "reason", "amount", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount


@staff_required
def manager_dashboard(request):
    if request.method == "POST":
        form = ChargeForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f"Added charge: {payment}.")
            return redirect("manager_dashboard")
    else:
        form = ChargeForm()

    houses = (
        House.objects
        .annotate(total_debt=Sum("payments__amount",
                                 filter=Q(payments__paid_date__isnull=True)))
        .prefetch_related("residents__user")
    )
    unpaid = (
        Payment.objects.filter(paid_date__isnull=True)
        .select_related("house")
        .order_by("due_date")
    )
    return render(request, "apartments/manager.html",
                  {"houses": houses, "unpaid": unpaid, "form": form})


@staff_required
@require_POST
def mark_paid(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if not payment.is_paid:
        payment.paid_date = timezone.localdate()
        payment.save(update_fields=["paid_date"])
        messages.success(request, f"Marked as paid: {payment}.")
    return redirect("manager_dashboard")
