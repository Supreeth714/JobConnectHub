# JobConnectHub 🚀

A production-ready full-stack **Job Portal** built with **Django + Django REST Framework**, with a clean LinkedIn-style UI using Django Templates + Bootstrap 5.

Two roles: **Candidate** and **Recruiter**.

---

## ✨ Features

### Candidate
- Register / Login (JWT + session)
- LinkedIn-style profile (name, skills, experience, resume, photo)
- Browse, search & filter jobs (title, skills, location)
- Apply for jobs
- Track application status (Applied / Shortlisted / Rejected)

### Recruiter
- Company profile (name, description, location)
- Create / Update / Delete job posts
- View applicants per job, filter by skills
- Shortlist / Reject applicants
- **Send emails** to candidates directly from the app

### Admin
- Manage users, jobs, applications via Django admin
- System stats on admin dashboard

### Backend
- Custom User model with `role` field (candidate/recruiter)
- DRF APIs with JWT (SimpleJWT)
- Role-based custom permissions
- Serializers + ViewSets
- Filters via `django-filter`

---

## 📁 Project Structure

```
jobconnecthub/
├── manage.py
├── requirements.txt
├── jobconnecthub/          # project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/               # users, profiles, auth
│   ├── models.py
│   ├── serializers.py
│   ├── views.py            # template views
│   ├── api_views.py        # DRF views
│   ├── urls.py
│   ├── api_urls.py
│   ├── permissions.py
│   ├── forms.py
│   └── admin.py
├── jobs/                   # jobs + companies
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── api_views.py
│   ├── urls.py
│   ├── api_urls.py
│   ├── forms.py
│   └── admin.py
├── applications/           # job applications + email
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── api_views.py
│   ├── urls.py
│   ├── api_urls.py
│   └── admin.py
├── api/                    # API root
│   └── urls.py
├── templates/              # all HTML templates
│   ├── base.html
│   ├── landing.html
│   ├── registration/
│   ├── accounts/
│   ├── jobs/
│   └── applications/
├── static/                 # CSS / JS
│   └── css/style.css
└── media/                  # uploaded files (resumes, photos)
```

---

## 🛠️ Setup Instructions

### 1. Clone / unzip and enter the folder
```bash
cd jobconnecthub
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations accounts jobs applications
python manage.py migrate
```

### 5. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

Visit:
- 🏠 App: http://127.0.0.1:8000/
- 🛡️ Admin: http://127.0.0.1:8000/admin/
- 📡 API root: http://127.0.0.1:8000/api/

---

## 📡 API Endpoints (DRF + JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register user (role = candidate / recruiter) |
| POST | `/api/auth/login/` | JWT login (returns access + refresh) |
| POST | `/api/auth/refresh/` | Refresh JWT |
| GET/PUT | `/api/accounts/profile/` | Get or update own profile |
| GET | `/api/jobs/` | List jobs (supports `?search=` & filters) |
| POST | `/api/jobs/` | Create job (recruiter only) |
| GET/PUT/DELETE | `/api/jobs/<id>/` | Job detail (PUT/DELETE = owner recruiter) |
| POST | `/api/applications/apply/<job_id>/` | Apply for a job (candidate) |
| GET | `/api/applications/mine/` | Candidate's own applications |
| GET | `/api/applications/job/<job_id>/` | Applicants for a job (recruiter) |
| PATCH | `/api/applications/<id>/status/` | Shortlist / Reject |
| POST | `/api/applications/<id>/email/` | Send email to candidate |

All protected endpoints require header:
```
Authorization: Bearer <access_token>
```

---

## 🔄 User Flow

1. Visitor lands on **/** → sees **JobConnectHub** logo + Login / Register.
2. Registers as **Candidate** or **Recruiter**.
3. Logs in → redirected to role-based dashboard:
   - **Candidate**: profile, browse/search jobs, apply, track applications.
   - **Recruiter**: company profile, post jobs, view applicants, shortlist/reject, email candidates.
4. When a recruiter changes status or sends an email, the candidate sees the update in their applications page (and gets an email if SMTP is configured).

---

## 📧 Email Configuration

By default, emails print to the console (dev mode).
To send real emails, edit `jobconnecthub/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'you@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'JobConnectHub <you@gmail.com>'
```

---

## 🎨 UI

- Bootstrap 5 + custom LinkedIn-inspired theme (blues, whites, soft shadows).
- Responsive navbar, sidebar on dashboards, card-based job listings.
- Clean typography (Inter font).

Enjoy building on top of **JobConnectHub**! 💼
