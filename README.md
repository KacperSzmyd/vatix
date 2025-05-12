# 📡 Vatix SOS Tracker – Backend Recruitment Task

This project is a simple backend system for tracking users and their SOS devices, built with Django and Django REST Framework.

---

## 🚀 Features

- Assign/unassign SOS devices to users
- Store location pings only when device is assigned
- Retrieve user’s last known location
- View live device positions on a map
- Prevent location spam with time delta check

---

## 🛠 Tech Stack

- Python 3.12
- Django 4.x
- Django REST Framework

---

## 📦 Setup Instructions

1. **Clone the repository** and navigate into the project folder:
   ```bash
    git clone <your-repo-url>
    cd <project-folder>
2. **Create virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows: venv\Scripts\activate
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
4. **Run migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
5. **Create superuser (optional):**
    ```bash
    python manage.py createsuperuser
6. **Run the development server:**
    ```bash
    python manage.py runserver


---
**📚 API Endpoints:**

🔄 Assign device to user
POST /devices/<device_id>/assign/

❌ Unassign device
POST /devices/<device_id>/unassign/

📍 Add location ping
POST /devices/<device_id>/location/

👤 Get user's last known location
GET /users/<user_id>/location/

🗺️ Get live map data
GET /map/

🧾 Get all devices and assignment status
GET /devices/

---

👨‍💻 Author
Kacper Szmyd – Junior Python Developer


---

“If I had more time, I would...”
I would add tests for every crucial functionality.  