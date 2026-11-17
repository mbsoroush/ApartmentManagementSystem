from django.contrib import admin
from .models import House, Resident, Payment


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ("number", "floor", "area", "rooms", "status")
    list_filter = ("status", "floor")


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ("user", "house", "phone")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("house", "reason", "amount", "due_date", "paid_date")
    list_filter = ("reason", "paid_date")
    date_hierarchy = "due_date"
