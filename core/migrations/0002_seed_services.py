from django.db import migrations

SERVICES = [
    # name, category, description, icon, price, order
    ("Plumbing", "Repairs", "Leaking taps, clogged drains, and pipe repairs.", "🔧", "From NPR 500", 1),
    ("Electrical", "Repairs", "Switches, wiring, lighting, and power issues.", "⚡", "From NPR 600", 2),
    ("Home cleaning", "Cleaning", "Make every room feel fresh, tidy, and welcoming.", "🧹", "From NPR 800", 3),
    ("Carpentry", "Repairs", "Furniture fixes, shelves, doors, and woodwork.", "🪚", "From NPR 700", 4),
    ("Appliance repair", "Repairs", "Help with common household appliance problems.", "🧰", "From NPR 700", 5),
    ("Painting", "Care", "Give your walls a fresh look with a neat finish.", "🖌️", "Request quote", 6),
    ("Installation", "Installation", "Mounting, fitting, and setting up household items.", "🪛", "From NPR 500", 7),
    ("Pest control", "Care", "Practical help for common household pest issues.", "🏡", "Request quote", 8),
]


def seed(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    for name, category, desc, icon, price, order in SERVICES:
        Service.objects.get_or_create(
            name=name,
            defaults=dict(category=category, short_description=desc, icon=icon, price_text=price, sort_order=order),
        )


def unseed(apps, schema_editor):
    apps.get_model("core", "Service").objects.filter(name__in=[s[0] for s in SERVICES]).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
