# TenantPro — Property Management System

A full-stack Django + MySQL property management application with role-based access for Admins, Property Owners, and Tenants.

## 🏗️ Project Structure

```
tenants_project/
├── core/               # Django project settings & URLs
├── accounts/           # Custom User model + Auth (signup/login)
├── owners/             # Owner profiles & management
├── tenants/            # Tenant profiles & lease management
├── properties/         # Property listings & CRUD
├── payments/           # Payment tracking & receipts
├── templates/          # All HTML templates
│   ├── base.html       # Shared sidebar layout
│   ├── accounts/       # Login, signup, profile
│   ├── owners/         # Owner profile forms
│   ├── tenants/        # Tenant forms & lease views
│   ├── properties/     # Property CRUD views
│   ├── payments/       # Payment forms & history
│   └── shared/         # Role-based dashboards
└── static/             # CSS, JS, images
```

## 🔑 User Roles

| Role   | Can Do |
|--------|--------|
| **Admin** | Full access — manage all users, properties, leases, payments |
| **Owner** | Add/edit own properties, create leases, record & view payments |
| **Tenant** | View own lease, browse available properties, view payment history |

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install django mysqlclient pillow
```

### 2. MySQL Setup

```bash
mysql -u root -p < mysql_setup.sql
```

Or manually in MySQL:
```sql
CREATE DATABASE tenants_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure MySQL in settings.py

Open `core/settings.py` and switch from SQLite to MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tenants_db',
        'USER': 'root',           # your MySQL user
        'PASSWORD': 'your_pass',  # your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

Or using the shell:
```bash
python manage.py shell -c "
from accounts.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
"
```

### 6. Start the Server

```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

## 🗺️ URL Routes

| URL | Description |
|-----|-------------|
| `/accounts/signup/` | User registration |
| `/accounts/login/` | Login |
| `/dashboard/` | Role-based dashboard redirect |
| `/dashboard/admin/` | Admin dashboard |
| `/dashboard/owner/` | Owner dashboard |
| `/dashboard/tenant/` | Tenant dashboard |
| `/owners/profile/create/` | Owner profile setup |
| `/tenants/profile/create/` | Tenant profile setup |
| `/properties/` | Property listings |
| `/properties/create/` | Add property (Owner) |
| `/tenants/leases/` | View leases |
| `/tenants/leases/create/` | Create lease (Owner/Admin) |
| `/payments/` | Payment history |
| `/payments/create/` | Record payment (Owner/Admin) |
| `/admin/` | Django admin panel |

## 🔄 User Flow

```
Register → Choose Role (Owner / Tenant)
    ↓
Login → Complete Profile (Owner/Tenant specific)
    ↓
Owner: Add Properties → Create Leases → Record Payments
Tenant: View Lease → Browse Properties → View Payment History
```

## 🗄️ Database Models

- **User** — Custom auth with role field (admin/owner/tenant)
- **Owner** — Extends User with Aadhaar, PAN, bank details
- **Tenant** — Extends User with occupation, employer, income
- **Property** — Linked to Owner; type, location, rent, amenities
- **Lease** — Links Tenant ↔ Property with dates and rent terms
- **Payment** — Linked to Lease; amount, method, receipt, status

## 🔐 Default Credentials (Development)

```
Username: admin
Password: admin123
Role: Admin
```
