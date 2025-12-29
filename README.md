# Ignite Learning Tracker — Django (monolithic)

A minimal, colorful learning tracker built with Django (server-rendered templates) and Tailwind (via CDN).  
Features: user auth (username/password), Dashboard, Notes, Topics, Projects, Tasks (simple Kanban), Milestones, Export/Import JSON backup, Light/Dark theme toggle.

Requirements
- Python 3.10+ (works with 3.8+ but recommended 3.10+)
- pip

Quick start (development)
1. Create & activate a virtualenv (recommended)
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows

2. Install requirements
   pip install -r requirements.txt

3. Apply migrations and create superuser
   python manage.py migrate
   python manage.py createsuperuser

4. Run dev server
   python manage.py runserver

5. Open http://127.0.0.1:8000/ and register/login

Notes
- Data is stored in local SQLite (db.sqlite3).
- Tailwind is loaded via CDN for quick prototyping (no Node build step).
- Export/Import available in Settings.

If you want production-ready Tailwind builds or deployment instructions, I can add them.