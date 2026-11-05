import re
from django import forms
from django.utils import timezone

from .models import Booking, Service


class BookingForm(forms.ModelForm):
    # "other" (or empty) means a service that isn't in the list.
    service = forms.CharField(required=True)

    class Meta:
        model = Booking
        fields = ["customer_name", "customer_phone", "service_date", "time_slot", "address", "details"]

    def clean_service(self):
        value = self.cleaned_data["service"].strip()
        if value == "other":
            return None
        try:
            return Service.objects.get(pk=int(value), is_active=True)
        except (ValueError, Service.DoesNotExist):
            raise forms.ValidationError("Please choose a valid service.")

    def clean_customer_name(self):
        return self.cleaned_data["customer_name"].strip()

    def clean_customer_phone(self):
        phone = self.cleaned_data["customer_phone"].strip()
        if not re.fullmatch(r"[0-9+ ()-]{7,16}", phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_service_date(self):
        chosen = self.cleaned_data["service_date"]
        if chosen < timezone.localdate():
            raise forms.ValidationError("Please choose today or a future date.")
        return chosen

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.service = self.cleaned_data["service"]
        if commit:
            booking.save()
        return booking
