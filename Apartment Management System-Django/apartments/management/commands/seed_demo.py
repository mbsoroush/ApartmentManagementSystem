from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apartments.models import House, Payment, Resident, StatusRequest

PASSWORD = "resident12345"

# number, floor, area, rooms, status
HOUSES = [(1, 1, 100, 2, "RENTED"), (2, 1, 70, 1, "RENTED"), (3, 2, 100, 2, "OWNED"),
          (4, 2, 70, 1, "EMPTY"), (5, 3, 120, 3, "OWNED"), (6, 3, 85, 2, "EMPTY")]

# username, first name, last name, house number
RESIDENTS = [("resident1", "Test", "Resident", 1), ("resident2", "Sara", "Karimi", 2),
             ("resident3", "Nima", "Hosseini", 3), ("resident4", "Mina", "Jafari", 5)]

# house, reason, amount, due date (days from today), already paid?
PAYMENTS = [
    (1, "ELECTRICITY", 120000, -45, True), (1, "GAS", 60000, -30, True),
    (1, "CHARGE", 200000, -10, False), (1, "WATER", 40000, 5, False),
    (2, "RENT", 3000000, -20, True), (2, "ELECTRICITY", 90000, -8, False),
    (2, "CHARGE", 200000, 12, False),
    (3, "CHARGE", 200000, -35, True), (3, "MORTGAGE", 1500000, -5, False),
    (3, "WATER", 35000, 9, False),
    (5, "CHARGE", 250000, -40, True), (5, "GAS", 75000, -3, True),
    (5, "ELECTRICITY", 140000, 7, False),
]


class Command(BaseCommand):
    help = "Create demo data: a manager, six houses, four residents, payments and requests."

    def handle(self, *args, **options):
        User = get_user_model()
        today = timezone.localdate()

        manager, created = User.objects.get_or_create(
            username="manager", defaults=dict(is_staff=True, is_superuser=True))
        if created:
            manager.set_password("manager12345")
            manager.save()

        houses = {}
        for number, floor, area, rooms, status in HOUSES:
            houses[number], _ = House.objects.get_or_create(
                number=number, defaults=dict(floor=floor, area=area, rooms=rooms))
            House.objects.filter(number=number).update(status=status)

        residents = {}
        for username, first, last, number in RESIDENTS:
            user, created = User.objects.get_or_create(
                username=username, defaults=dict(first_name=first, last_name=last))
            if created:
                user.set_password(PASSWORD)
                user.save()
            residents[username], _ = Resident.objects.get_or_create(
                user=user, defaults=dict(house=houses[number]))

        for number, reason, amount, offset, paid in PAYMENTS:
            if Payment.objects.filter(house=houses[number], reason=reason).exists():
                continue
            due = today + timedelta(days=offset)
            Payment.objects.create(
                house=houses[number], reason=reason, amount=amount, due_date=due,
                paid_date=due + timedelta(days=1) if paid else None)

        StatusRequest.objects.get_or_create(
            resident=residents["resident2"], status="PENDING",
            defaults=dict(requested_status="OWNED", note="I would like to buy the apartment."))
        StatusRequest.objects.get_or_create(
            resident=residents["resident3"], status="PENDING",
            defaults=dict(requested_status="EMPTY", note="Moving out at the end of the month."))

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
