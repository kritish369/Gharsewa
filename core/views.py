from logging import config

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import Booking, Service
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    services = Service.objects.filter(is_active=True)
    return render(request, "index.html", {
        "services": services,
        "time_slots": Booking.TimeSlot.choices,
        "categories": Service.Category.choices,
    })


@require_POST
def book(request):
    
        
    form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save()
        service = booking.service.name if booking.service else "your home service"
        customer_mail = form.cleaned_data.get('customer_email')
        send_mail(
            subject="New Booking Request",
            message=f"New booking request from {booking.customer_name} for {service} on {booking.service_date}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER, customer_mail]
        )
        return JsonResponse({
            "ok": True,
            "message": f"Thanks, {booking.customer_name}! Your request for {service} has been received.",
        })
    
    
    errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
    return JsonResponse({"ok": False, "errors": errors}, status=400)



