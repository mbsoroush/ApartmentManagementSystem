from django.conf import settings
from django.db import models
from django.utils import timezone


class House(models.Model):
    class Status(models.TextChoices):
        EMPTY = "EMPTY", "Empty"
        RENTED = "RENTED", "Rented"
        OWNED = "OWNED", "Owned"

    number = models.PositiveIntegerField(unique=True)
    floor = models.PositiveIntegerField()
    area = models.PositiveIntegerField(help_text="Area in square meters")
    rooms = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.EMPTY)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"House {self.number} (floor {self.floor})"


class Resident(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="residents")
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Payment(models.Model):
    class Reason(models.TextChoices):
        ELECTRICITY = "ELECTRICITY", "Electricity bill"
        WATER = "WATER", "Water bill"
        GAS = "GAS", "Gas bill"
        RENT = "RENT", "Rent"
        CHARGE = "CHARGE", "Apartment charge"
        MORTGAGE = "MORTGAGE", "Mortgage"

    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="payments")
    reason = models.CharField(max_length=20, choices=Reason.choices)
    amount = models.PositiveIntegerField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-due_date"]

    @property
    def is_paid(self):
        return self.paid_date is not None

    @property
    def is_overdue(self):
        return not self.is_paid and self.due_date < timezone.localdate()

    def __str__(self):
        return f"{self.get_reason_display()} {self.amount} for {self.house}"


class StatusRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    resident = models.ForeignKey(Resident, on_delete=models.CASCADE,
                                 related_name="requests")
    requested_status = models.CharField(max_length=10, choices=House.Status.choices)
    note = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices,
                              default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (f"{self.resident}: {self.get_requested_status_display()} "
                f"({self.get_status_display()})")
