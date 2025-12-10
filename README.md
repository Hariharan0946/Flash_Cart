# 🚚 FlashCart – 10-Minute Delivery Backend

FlashCart is a **backend-only Django project** that simulates the core backend of a **quick-commerce / 10-minute delivery app** (similar to Blinkit, Zepto, Instamart).

This project focuses on **backend engineering concepts**, not frontend UI.

It was built to understand and demonstrate:
- how real backend systems are structured  
- how users, products, and orders interact  
- how real-time tracking works  
- how background tasks, caching, and deployment are handled  

---

## 🧠 What does this project do? (Simple explanation)

FlashCart allows:

- Users to **sign up and log in** using JWT authentication  
- Admins to **add products and manage stock**  
- Users to **place orders**  
- Orders to move through multiple states (placed → packed → delivered)  
- Delivery updates to be sent **in real time** using WebSockets  
- Background tasks (like auto-cancel or updates) to run using Celery  
- Frequently used data to be cached using Redis  

No frontend is required — all features work via APIs.

---

## 🧱 Project Structure
Flash_Cart/
│
├── flashcart/ # Main Django project (settings, urls, asgi)
├── users/ # User authentication & JWT logic
├── products/ # Product and inventory management
├── orders/ # Order creation and order workflow
├── tracking/ # WebSocket logic for real-time tracking
│
├── scripts/ # Helper shell scripts
├── tests/ # Basic test cases
├── fixtures/ # Sample data
├── logs/ # Log files
│
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── Makefile
├── VERSION
├── requirements.txt
├── .env.example
└── README.md
---

## 🔐 Authentication (users app)

- Uses **JWT (JSON Web Tokens)**  
- Supports login, refresh token, and logout  
- Token blacklist enabled for logout  

JWT is used because it is:
- Stateless  
- Scalable  
- Common in real-world APIs  

---

## 📦 Products & Inventory (products app)

- Create and update products  
- Maintain stock count  
- Prevent orders when stock is not available  

This simulates inventory systems used in real delivery apps.

---

## 🛒 Orders (orders app)

- Users can place orders  
- Orders follow a workflow:

PLACED → PACKED → OUT_FOR_DELIVERY → DELIVERED

yaml
Copy code

- Orders can be cancelled under defined rules  
- Background jobs can update order status  

---

## 📍 Real-Time Tracking (tracking app)

- Implemented using **Django Channels (WebSockets)**  
- Clients can subscribe to an order’s tracking channel  
- Delivery updates are pushed live without polling  

Important files:
- `tracking/consumers.py`
- `flashcart/routing.py`
- `flashcart/asgi.py`

---

## ⚙️ Background Tasks (Celery)

Used for tasks that should not block the main API:

- Auto-cancel stale orders  
- Notifications  
- Status updates  

Uses:
- **Celery**
- **Redis** as the message broker  

---

## ⚡ Redis Usage

Redis is used for:
- Caching frequently accessed data  
- Message broker for Celery  
- Channel layer for WebSockets  

This improves speed and scalability.

---

## 🗄 Database

- PostgreSQL database  
- Django migrations used  
- Environment-based configuration  

Supports both:
- Local development
- Deployment using `DATABASE_URL`

---

## 🐳 Docker & Local Setup

The project is fully dockerized.

Services include:
- Django backend  
- PostgreSQL  
- Redis  
- Celery worker  
- Celery beat  

Run locally using:
docker-compose up --build

yaml
Copy code

---

## 🧪 Testing

- Basic tests included in `tests/`  
- Fixtures provided for sample data  
- Tests focus on core flows (auth, products, orders)

---

## 📄 Environment Variables

Refer to `.env.example` for required variables:

DEBUG
SECRET_KEY
DATABASE_URL
REDIS_URL
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD

yaml
Copy code

---

## 📚 Key Concepts Demonstrated

- REST API development  
- JWT authentication  
- Background processing  
- Redis caching  
- WebSockets for real-time updates  
- Docker-based development  
- Environment-driven configuration  

---

## 👨‍💻 Author

**Hariharan Balasubramaniyam**  
Backend Developer (Python • Django • DSA)

---

## ✅ Final Note

This project is a **learning and demonstration backend project** built to understand how **real backend systems** work together.

It reflects real-world backend design decisions and trade-offs.
It is not a perfect production system, but it reflects real-world backend design decisions and tradeoffs.
