# 🐔 PoultrySync — Multi-Tenant Ordering System

A Django-based backend for managing products and orders in a multi-tenant environment, built for the PoultrySync technical assessment.

---

## 🚀 Features

- 🔐 Role-based access control (Admin, Operator, Viewer)
- 🏢 Multi-tenancy (data scoped per Company)
- 📦 Product and Order management with stock validation
- ❌ Soft delete for products
- 📄 CSV export for company orders
- 📬 Order success logs simulate confirmation emails
- 🖥️ Simple front-end form at `/` for adding and viewing products
- 🐳 Dockerized with MySQL 5.7

---

## 🛠️ Tech Stack

- Python 3.11+
- Django 4.2+
- MySQL 5.7
- Django REST Framework
- Docker + docker-compose

---

## 🧱 Setup Instructions

### 🐳 Docker (Recommended)

1. Clone the repo:
   ```bash
   git clone https://github.com/MahmoudGShake/poultrysync.git
   cd poultrysync
   ```

2. Start the stack:
   ```bash
   docker-compose up --build
   ```

3. The app will be available at:
   - `http://localhost:8000` (Product form and table)
   - `http://localhost:8000/admin/` (Django Admin)

---

## 🔐 Demo Credentials

| Role     | Username        | Password     |
|----------|------------------|--------------|
| Admin    | `admin`     | `admin123`   |
| Operator | `operator`  | `operator123`|
| Viewer   | `viewer`    | `viewer123`  |

---

## 🧪 Seed Demo Data

Run this after migrations:

```bash
python manage.py seed_demo
```

It will create:

- A company `DemoCorp`
- 3 users (admin/operator/viewer)
- 5 products
- 3 orders

---

## 🔄 API Endpoints

| Endpoint                  | Method | Access       | Description                    |
|---------------------------|--------|--------------|--------------------------------|
| `/api/products/`          | GET    | all          | List active products           |
| `/api/products/`          | POST   | admin/operator | Create product               |
| `/api/products/{id}/`     | DELETE | admin/operator | Soft-delete product         |
| `/api/orders/`            | GET    | all          | List orders                    |
| `/api/orders/`            | POST   | admin/operator | Create order (stock checked) |
| `/api/orders/export/`     | GET    | admin/operator | Download CSV of orders      |

---

## 📄 Logging

Order confirmations (`status = success`) are logged to:

```
logs/orders.log
```

Each entry simulates an order email confirmation.

---

## 📁 Project Structure

```
poultrysync/
├── orders/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── urls.py
│   ├── forms.py
│   └── management/commands/seed_demo.py
├── templates/orders/index.html
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ✅ To Do

- [x] Multi-tenant support
- [x] Role-based access
- [x] Soft delete & CSV export
- [x] Product form + table
- [x] Dockerized setup
- [x] Demo data seeder

---

## 👤 Author

Built with ❤️ by Mahmoud Gamal for the PoultrySync Back-end Engineer assessment.