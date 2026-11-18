from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import House, Payment, Resident, StatusRequest

User = get_user_model()
PASSWORD = "pw12345!"


class BaseTestCase(TestCase):
    def setUp(self):
        self.house = House.objects.create(
            number=1, floor=1, area=100, rooms=2, status="RENTED")
        self.other_house = House.objects.create(
            number=2, floor=1, area=70, rooms=1, status="EMPTY")
        self.user = User.objects.create_user("res", password=PASSWORD)
        self.resident = Resident.objects.create(user=self.user, house=self.house)
        self.manager = User.objects.create_user(
            "mgr", password=PASSWORD, is_staff=True)

    def login_resident(self):
        self.client.login(username="res", password=PASSWORD)

    def login_manager(self):
        self.client.login(username="mgr", password=PASSWORD)

    def pay(self, reason="WATER", amount=100, due=date(2026, 10, 1), paid=None,
            house=None):
        return Payment.objects.create(
            house=house or self.house, reason=reason, amount=amount,
            due_date=due, paid_date=paid)


class PaymentModelTests(BaseTestCase):
    def test_unpaid_past_due_payment_is_overdue(self):
        p = self.pay(due=date(2020, 1, 1))
        self.assertFalse(p.is_paid)
        self.assertTrue(p.is_overdue)

    def test_paid_payment_is_not_overdue(self):
        p = self.pay(due=date(2020, 1, 1), paid=date(2020, 1, 2))
        self.assertTrue(p.is_paid)
        self.assertFalse(p.is_overdue)

    def test_unpaid_future_payment_is_not_overdue(self):
        p = self.pay(due=timezone.localdate() + timedelta(days=5))
        self.assertFalse(p.is_overdue)


class ResidentDashboardTests(BaseTestCase):
    def test_login_required(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_total_debt_counts_only_unpaid_payments_of_own_house(self):
        self.pay(amount=100)
        self.pay(amount=200)
        self.pay(amount=500, paid=date(2026, 10, 2))
        self.pay(amount=999, house=self.other_house)
        self.login_resident()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.context["total_debt"], 300)
        self.assertEqual(len(response.context["history"]), 3)

    def test_filter_by_reason(self):
        self.pay(reason="WATER")
        self.pay(reason="GAS")
        self.login_resident()
        response = self.client.get(reverse("dashboard"), {"reason": "GAS"})
        history = list(response.context["history"])
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].reason, "GAS")

    def test_date_filter_includes_both_boundary_dates(self):
        self.pay(due=date(2026, 10, 1))
        self.pay(due=date(2026, 11, 1))
        self.login_resident()
        response = self.client.get(
            reverse("dashboard"),
            {"date_from": "2026-10-01", "date_to": "2026-10-01"})
        self.assertEqual(len(response.context["history"]), 1)

    def test_manager_without_house_is_sent_to_manager_page(self):
        self.login_manager()
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("manager_dashboard"))


class StatusRequestTests(BaseTestCase):
    def send(self, status):
        return self.client.post(
            reverse("submit_request"), {"requested_status": status, "note": "hi"})

    def test_resident_can_request_allowed_change(self):
        self.login_resident()
        self.send("OWNED")
        self.assertEqual(StatusRequest.objects.count(), 1)
        self.assertEqual(StatusRequest.objects.get().status, "PENDING")

    def test_cannot_request_current_status(self):
        self.login_resident()
        self.send("RENTED")
        self.assertEqual(StatusRequest.objects.count(), 0)

    def test_cannot_request_invalid_status(self):
        self.login_resident()
        self.send("NONSENSE")
        self.assertEqual(StatusRequest.objects.count(), 0)

    def test_only_one_pending_request_at_a_time(self):
        self.login_resident()
        self.send("OWNED")
        self.send("EMPTY")
        self.assertEqual(StatusRequest.objects.count(), 1)

    def test_manager_approval_updates_house_status(self):
        req = StatusRequest.objects.create(
            resident=self.resident, requested_status="OWNED")
        self.login_manager()
        self.client.post(reverse("decide_request", args=[req.pk, "approve"]))
        req.refresh_from_db()
        self.house.refresh_from_db()
        self.assertEqual(req.status, "APPROVED")
        self.assertEqual(self.house.status, "OWNED")

    def test_manager_rejection_keeps_house_status(self):
        req = StatusRequest.objects.create(
            resident=self.resident, requested_status="OWNED")
        self.login_manager()
        self.client.post(reverse("decide_request", args=[req.pk, "reject"]))
        req.refresh_from_db()
        self.house.refresh_from_db()
        self.assertEqual(req.status, "REJECTED")
        self.assertEqual(self.house.status, "RENTED")


class ManagerPermissionTests(BaseTestCase):
    def test_resident_cannot_open_manager_page(self):
        self.login_resident()
        response = self.client.get(reverse("manager_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_resident_cannot_mark_payment_paid(self):
        p = self.pay()
        self.login_resident()
        response = self.client.post(reverse("mark_paid", args=[p.pk]))
        self.assertEqual(response.status_code, 403)
        p.refresh_from_db()
        self.assertIsNone(p.paid_date)

    def test_manager_can_mark_payment_paid(self):
        p = self.pay()
        self.login_manager()
        self.client.post(reverse("mark_paid", args=[p.pk]))
        p.refresh_from_db()
        self.assertEqual(p.paid_date, timezone.localdate())

    def test_manager_can_add_charge(self):
        self.login_manager()
        self.client.post(reverse("manager_dashboard"), {
            "house": self.house.pk, "reason": "GAS", "amount": 5000,
            "due_date": "2026-12-01"})
        self.assertEqual(Payment.objects.filter(reason="GAS").count(), 1)

    def test_charge_with_zero_amount_is_rejected(self):
        self.login_manager()
        self.client.post(reverse("manager_dashboard"), {
            "house": self.house.pk, "reason": "GAS", "amount": 0,
            "due_date": "2026-12-01"})
        self.assertEqual(Payment.objects.count(), 0)
