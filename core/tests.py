from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Booking, Service


class HomeAndBookingTests(TestCase):
    def test_home_lists_seeded_services_and_css(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Plumbing")
        self.assertContains(response, "/static/css/style.css")
        self.assertEqual(Service.objects.count(), 8)

    def _payload(self, **overrides):
        data = {
            "service": str(Service.objects.get(name="Plumbing").pk),
            "customer_name": "Anil Sharma",
            "customer_phone": "9800000000",
            "service_date": (timezone.localdate() + timedelta(days=1)).isoformat(),
            "time_slot": Booking.TimeSlot.MORNING,
            "address": "Baneshwor, Kathmandu",
            "details": "Leaking tap",
        }
        data.update(overrides)
        return data

    def test_valid_booking_is_saved(self):
        response = self.client.post(reverse("book"), self._payload())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        booking = Booking.objects.get()
        self.assertEqual(booking.service.name, "Plumbing")
        self.assertEqual(booking.status, "pending")

    def test_other_service_saves_without_service(self):
        self.client.post(reverse("book"), self._payload(service="other"))
        self.assertIsNone(Booking.objects.get().service)

    def test_past_date_and_bad_phone_rejected(self):
        past = (timezone.localdate() - timedelta(days=1)).isoformat()
        response = self.client.post(reverse("book"), self._payload(service_date=past, customer_phone="abc"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("service_date", response.json()["errors"])
        self.assertIn("customer_phone", response.json()["errors"])
        self.assertEqual(Booking.objects.count(), 0)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(reverse("book")).status_code, 405)
