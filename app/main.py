from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# --- Direct Imports to Avoid 'NoneType' or Initialization Errors ---
# This is the safest way to ensure each router is properly loaded.
from app.api.routes.auth import router as auth_router
from app.api.routes.bills import router as bills_router
from app.api.routes.rewards import router as rewards_router
from app.api.routes.accounts import router as accounts_router
from app.api.routes.insights import router as insights_router
from app.api.routes.alerts import router as alerts_router

# Import Automation Scheduler for Background Jobs
from app.core.scheduler import start_scheduler

# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------
# This creates all tables (Users, Transactions, Budgets, Alerts) on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Modern Digital Banking Dashboard API",
    description="Backend API for Milestone 4 - Insights, Alerts, and Automation",
    version="4.0.0"
)

# ---------------------------------------------------------
# 1. Configure CORS (Cross-Origin Resource Sharing)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. Register Milestone 1-4 Routers
# ---------------------------------------------------------
# We use the aliased names (e.g., auth_router) to avoid naming conflicts
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(bills_router, prefix="/bills", tags=["Bill Management"])
app.include_router(rewards_router, prefix="/rewards", tags=["Rewards Program"])
app.include_router(accounts_router, prefix="/accounts", tags=["Account Management"])
app.include_router(insights_router, prefix="/insights", tags=["Insights & Analytics"])
app.include_router(alerts_router, prefix="/alerts", tags=["Alert System"])

# ---------------------------------------------------------
# 3. Startup Event: Initialize Background Automation
# ---------------------------------------------------------
@app.on_event("startup")
def on_startup():
    """
    Triggers when the FastAPI server launches. 
    Starts the APScheduler to run background logic for financial checks.
    """
    try:
        start_scheduler()
        print("🚀 SUCCESS: Milestone 4 Background Job Scheduler Started.")
        print("📡 MONITORING: Automated checks for Low Balance and Budgets are active.")
    except Exception as e:
        print(f"❌ ERROR: Automation Engine failed to start: {e}")

# ---------------------------------------------------------
# 4. Health Check Endpoint
# ---------------------------------------------------------
@app.get("/", tags=["System"])
def health_check():
    return {
        "status": "online",
        "version": "4.0.0",
        "milestone": 4,
        "message": "Modern Digital Banking Backend is fully operational."
    }