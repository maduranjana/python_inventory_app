# Inventory Management System

A full-stack inventory management system that includes user authentication, order and quotation handling, and inventory tracking. Built with **Flask (Python)** for backend APIs and **HTML/CSS/JS** for frontend.

## Features

- ✅ User Registration and Login (with hashed passwords)
- 📦 Inventory Management (Add, View, Edit inventory items)
- 🧾 Quotation Requests (Add, List)
- 🛒 Orders (Create, View)
- 🔐 Role-based Access (Admin, Supplier, etc.)

---

## Tech Stack

| Layer     | Technology            |
|-----------|------------------------|
| Backend   | Python Flask (REST API) |
| Frontend  | HTML, CSS, JavaScript   |
| Database  | MySQL                   |

---

## API Endpoints

### 🔐 Authentication

- `POST /api/login` – User login  
- `POST /api/register` – User registration

### 📦 Inventory

- `GET /inventory` – Get all inventory items  
- `POST /inventory` – Add new inventory item

### 🧾 Quotations

- `GET /quotations` – Get all quotations  
- `POST /quotations` – Add new quotation

### 🛒 Orders

- `GET /orders` – Get all orders  
- `POST /orders` – Create new order

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/inventory-system.git
   cd inventory-system
2. Install dependencies:

3.pip install -r requirements.txt
Create a .env or update db_config.py with your MySQL credentials.

4. Run the application:

python app.py
Open index.html in your browser to start using the system.

.
├── app.py
├── db_config.py
├── auth_routes.py
├── order_routes.py
├── quotation_routes.py
├── inventory_routes.py
├── static/
│   └── (CSS, JS, Images)
├── templates/
│   └── (HTML pages)
└── README.md
