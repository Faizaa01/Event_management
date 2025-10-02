# Event Management System

A **Django-based full-stack web application** for creating, managing, and viewing events.  
Users can sign up, create events, and explore upcoming events through a clean, responsive interface.

---

## Features
- User authentication: sign up, log in, log out
- Event creation and management
- Event listing and detail views
- Admin dashboard for managing events and users
- Responsive design using HTML, CSS, and optional Bootstrap

---

## Tech Stack
- **Backend:** Django
- **Frontend:** Django Templates, HTML, CSS, JS
- **Database:** SQLite (development) / PostgreSQL/MySQL (production)
- **Deployment:** Render

---

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/event-management.git
   cd event-management
    ````

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:

   ```bash
   python manage.py migrate
   ```
5. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```
6. Run the server:

   ```bash
   python manage.py runserver
   ```
7. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser

---
## License

MIT License – see [LICENSE](LICENSE)

---

