from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone

from .models import House, Payment, Resident, StatusRequest


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ("number", "floor", "area", "rooms", "status", "total_debt")
    list_filter = ("status", "floor")
    inlines = [PaymentInline]

    @admin.display(description="Total debt (Toman)")
    def total_debt(self, obj):
        total = obj.payments.filter(paid_date__isnull=True).aggregate(t=Sum("amount"))["t"]
        return total or 0


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ("user", "house", "phone")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("house", "reason", "amount", "due_date", "paid_date", "paid")
    list_filter = ("reason", "paid_date")
    date_hierarchy = "due_date"
    actions = ["mark_paid"]

    @admin.display(boolean=True, description="Paid")
    def paid(self, obj):
        return obj.is_paid

    @admin.action(description="Mark selected payments as paid today")
    def mark_paid(self, request, queryset):
        updated = queryset.filter(paid_date__isnull=True).update(
            paid_date=timezone.localdate())
        self.message_user(request, f"{updated} payment(s) marked as paid.")


@admin.register(StatusRequest)
class StatusRequestAdmin(admin.ModelAdmin):
    list_display = ("resident", "requested_status", "status", "created_at")
    list_filter = ("status",)
