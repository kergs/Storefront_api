# Storefront API

A production-ready e-commerce REST API built with Django and Django REST 
Framework, deployed on AWS EC2 with PostgreSQL on RDS. Infrastructure 
provisioned with Terraform.

> **Infrastructure:** See [storefront-infra](https://github.com/kergs/storefront-infra) 
> for the Terraform code that provisions the AWS infrastructure this API runs on.

---

## Live Deployment

| Component | Technology |
|---|---|
| Application Server | AWS EC2 (t3.micro) |
| Database | AWS RDS PostgreSQL |
| Web Server | Nginx + Gunicorn |
| Infrastructure | Terraform |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.2 LTS + Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL |
| Web Server | Nginx + Gunicorn |
| Environment | python-environ |
| Deployment | AWS EC2 + RDS |

---

## Architecture

Client Request
↓
Nginx (port 80)          ← Reverse proxy, static files
↓
Gunicorn (port 8000)     ← WSGI application server
↓
Django REST Framework    ← API logic, JWT auth
↓
AWS RDS PostgreSQL       ← Managed database (private subnet)
RDS lives in a **private subnet** — it is never exposed to the internet. 
Only the EC2 instance can talk to it via security group rules.

---

## API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | None | Register new user, returns JWT tokens |
| POST | `/api/auth/login/` | None | Login, returns JWT tokens |
| POST | `/api/auth/token/refresh/` | None | Refresh access token |

### Products
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/products/` | None | List all products |
| GET | `/api/products/?search=name` | None | Search products by name |
| GET | `/api/products/?category=slug` | None | Filter by category |
| GET | `/api/products/{id}/` | None | Get single product |
| POST | `/api/products/` | Admin | Create product |
| PUT | `/api/products/{id}/` | Admin | Update product |
| DELETE | `/api/products/{id}/` | Admin | Delete product |

### Categories
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/categories/` | None | List all categories |
| POST | `/api/categories/` | Admin | Create category |

### Orders
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/orders/` | JWT | Create order |
| GET | `/api/orders/` | JWT | Get user's orders |
| GET | `/api/orders/{id}/` | JWT | Get single order |

---

## Example Requests

### Register
```json
POST /api/auth/register/
{
    "username": "john",
    "email": "john@example.com",
    "password": "securepassword"
}
```

### Response
```json
{
    "message": "User created successfully",
    "username": "john",
    "email": "john@example.com",
    "access": "eyJhbGci...",
    "refresh": "eyJhbGci..."
}
```

### Create Order
```json
POST /api/orders/
Authorization: Bearer <access_token>

{
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ]
}
```

### Response
```json
{
    "id": 1,
    "username": "john",
    "status": "pending",
    "total": "199.98",
    "items": [
        {
            "product": {
                "id": 1,
                "name": "Wireless Headphones",
                "price": "99.99"
            },
            "quantity": 2,
            "price_at_purchase": "99.99",
            "subtotal": "199.98"
        }
    ],
    "created_at": "2026-05-14T13:35:01Z"
}
```

---

## Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/kergs/Storefront_api.git
cd Storefront_api
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:

### 5. Create PostgreSQL database
```bash
psql -U postgres
CREATE DATABASE storefront;
\q
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```

### 8. Run server
```bash
python manage.py runserver
```

API available at `http://localhost:8000`  
Admin panel at `http://localhost:8000/admin`

---

## Deployment

This API is deployed on AWS using the following setup:

1. **Terraform** provisions VPC, EC2, RDS, and security groups
2. **GitHub** hosts the code
3. **EC2** clones the repo and runs Gunicorn as a systemd service
4. **Nginx** sits in front of Gunicorn as a reverse proxy
5. **RDS** provides managed PostgreSQL in a private subnet

See [storefront-infra](https://github.com/kergs/storefront-infra) for 
full infrastructure code.

---

## Infrastructure Decisions

**Why EC2 + RDS over Heroku?**
EC2 gives full control over the server environment. RDS provides automated 
backups, failover, and patching — running PostgreSQL inside EC2 would 
require managing all of that manually. The combination is what most 
production Django applications use.

**Why JWT over session auth?**
JWT is stateless — the server doesn't need to store session data. This 
makes the API scalable across multiple servers without a shared session 
store. It's also the standard for REST APIs consumed by mobile apps and 
frontends.

**Why price_at_purchase on OrderItem?**
Product prices change over time. Storing the price at the moment of 
purchase ensures order history is always accurate regardless of future 
price changes — a critical requirement for any real e-commerce system.

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Set to `False` in production |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host (localhost or RDS endpoint) |
| `DB_PORT` | Database port (default: 5432) |

---

## Author

Built by [Chisom Okeke](https://github.com/kergs)  
📫 cchisomfrancis@gmail.com · 🐦 [@_kergs](https://twitter.com/_kergs)