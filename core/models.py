from django.db import models


class Service(models.Model):
    class Category(models.TextChoices):
        REPAIRS = "Repairs", "Repairs"
        CLEANING = "Cleaning", "Cleaning"
        INSTALLATION = "Installation", "Installation"
        CARE = "Care", "Home care"

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    short_description = models.CharField(max_length=200, help_text="Shown on the service card and used by search.")
    icon = models.CharField(max_length=8, default="🔧", help_text="An emoji shown on the card.")
    price_text = models.CharField(max_length=50, default="Request quote", help_text='e.g. "From NPR 500"')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    class TimeSlot(models.TextChoices):
        MORNING = "Morning (8 AM – 12 PM)", "Morning (8 AM – 12 PM)"
        AFTERNOON = "Afternoon (12 PM – 4 PM)", "Afternoon (12 PM – 4 PM)"
        EVENING = "Evening (4 PM – 7 PM)", "Evening (4 PM – 7 PM)"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    service = models.ForeignKey(
        Service, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings",
        help_text="Empty means 'Other home service'.",
    )
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    service_date = models.DateField()
    time_slot = models.CharField(max_length=40, choices=TimeSlot.choices)
    address = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        service = self.service.name if self.service else "Other home service"
        return f"{self.customer_name} – {service} on {self.service_date}"
