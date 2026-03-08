from fastapi import FastAPI
from app.database import engine, Base

# --- MODEL IMPORTS ---
# Explicitly importing ensures SQLAlchemy registers metadata for each table
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category_rule import CategoryRule
from app.models.budget import Budget
from app.models.alert import Alert

# --- ROUTER IMPORTS ---
from app.api.routes import auth, account, reports

# 1. Sync Database Schema
# Creates tables in the database based on the imported model classes
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Modern Digital Banking API",
    description="Milestone 2 Intelligence Engine: Automated Categorization, Budgeting, and Alerts",
    version="2.0.0"
)

# 2. Registering Routers
app.include_router(auth.router, prefix="/auth", tags=["Identity & Auth"])
app.include_router(account.router, prefix="/accounts", tags=["Banking Core"])
app.include_router(reports.router, prefix="/reports", tags=["Intelligence Engine"])

@app.get("/", tags=["Health Check"])
def read_root():
    """Returns the API status and current development milestone."""
    return {
        "status": "online",
        "milestone": 2,
        "message": "Intelligence engine is live and all database tables are synced."
    }