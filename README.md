# Modern Digital Banking Backend - Milestone 2

## 🚀 Project Overview
This project is a high-performance Banking API built with **FastAPI** and **PostgreSQL**. 
Milestone 2 focuses on a core **Intelligence Engine** that automates financial management for users.

## 🛠️ Key Features (Milestone 2)
* **Security:** Full JWT Authentication (Sign-up/Login) with protected banking routes.
* **Intelligence Engine:** Automated transaction categorization using a dual-priority Rule Engine (Exact vs. Keyword matching).
* **Data Integrity:** Automated database schema synchronization using SQLAlchemy.
* **Modular Architecture:** Clean separation between Models, Services, and API Routes.

## 📁 Project Structure
- `app/api/`: Contains authentication logic and transaction endpoints.
- `app/models/`: Database tables for Users, Transactions, and Category Rules.
- `app/services/`: The "Brain" of the app (Rule Engine logic).
- `app/schemas/`: Data validation using Pydantic.

## ⚙️ How to Run Locally
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`.
3. Activate it: `venv\Scripts\activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Start the server: `uvicorn app.main:app --reload`.

## 🧪 Testing the "Golden Path"
1. Register a user at `/auth/register`.
2. Login at `/auth/login` to receive a JWT Token.
3. Create a Category Rule at `/api/reports/rules`.
4. Post a raw transaction at `/accounts/transactions/` and watch the category auto-assign!