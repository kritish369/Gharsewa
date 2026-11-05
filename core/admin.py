from django.contrib import admin

from .models import Booking, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_text", "is_active", "sort_order")
    list_filter = ("category", "is_active")
    list_editable = ("is_active", "sort_order")
    search_fields = ("name", "short_description")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "customer_phone", "service", "service_date", "time_slot", "status", "created_at")
    list_filter = ("status", "service", "service_date")
    list_editable = ("status",)
    search_fields = ("customer_name", "customer_phone", "address")
    date_hierarchy = "service_date"
