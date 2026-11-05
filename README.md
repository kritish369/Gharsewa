# GharSewa

Django project: home-services landing page with a real booking database (SQLite).

## Run it
```bash
python -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ (site) and http://127.0.0.1:8000/admin/ (manage services and bookings).

## Layout
- `config/`  project settings and root URLs
- `core/`    models (Service, Booking), views, forms, admin
- `templates/index.html`  the page (Django template)
- `static/css/style.css`  the stylesheet
