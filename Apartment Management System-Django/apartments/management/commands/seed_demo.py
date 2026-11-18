from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apartments.models import House, Payment, Resident


class Command(BaseCommand):
    help = "Create demo data: a manager, four houses, a resident and some payments."

    def handle(self, *args, **options):
        User = get_user_model()

        manager, created = User.objects.get_or_create(
            username="manager", defaults=dict(is_staff=True, is_superuser=True))
        if created:
            manager.set_password("manager12345")
            manager.save()

        houses = {}
        for number, floor, area, rooms in [(1, 1, 100, 2), (2, 1, 70, 1),
                                           (3, 2, 100, 2), (4, 2, 70, 1)]:
            houses[number], _ = House.objects.get_or_create(
                number=number,
                defaults=dict(floor=floor, area=area, rooms=rooms, status="EMPTY"))
        House.objects.filter(number=1).update(status="RENTED")

        user, created = User.objects.get_or_create(
            username="resident1",
            defaults=dict(first_name="Test", last_name="Resident"))
        if created:
            user.set_password("resident12345")
            user.save()
        Resident.objects.get_or_create(user=user, defaults=dict(house=houses[1]))

        Payment.objects.get_or_create(
            house=houses[1], reason="ELECTRICITY", amount=120000,
            due_date=date(2026, 10, 1), defaults=dict(paid_date=date(2026, 10, 3)))
        Payment.objects.get_or_create(
            house=houses[1], reason="GAS", amount=60000,
            due_date=date(2026, 10, 15), defaults=dict(paid_date=date(2026, 10, 16)))
        Payment.objects.get_or_create(
            house=houses[1], reason="CHARGE", amount=200000, due_date=date(2026, 11, 1))

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
