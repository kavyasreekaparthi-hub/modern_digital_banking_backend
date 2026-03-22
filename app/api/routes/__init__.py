# app/api/routes/__init__.py

# --- Milestones 1-3 Routers ---
# These are the legacy routes for Authentication, Bills, and Rewards.
from .auth import router as auth
from .bills import router as bills
from .rewards import router as rewards

# --- Milestone 4 Routers (Core Logic & Serving Layers) ---
# Explicitly importing the new Milestone 4 logic.
# If 'accounts.py' is missing, the app will now throw a clear error 
# instead of a silent 'NoneType' crash.
from .accounts import router as accounts
from .insights import router as insights
from .alerts import router as alerts

# --- Milestone 4 Data Export (CSV/PDF) ---
# We use a try-except block here because Export is often the last 
# feature implemented. This keeps the rest of the app running.
try:
    from .export import router as export
except (ImportError, ModuleNotFoundError):
    export = None

# ---------------------------------------------------------
# The __all__ list ensures that 'from app.api.routes import *' 
# or direct package imports in main.py work flawlessly.
# ---------------------------------------------------------
__all__ = [
    "auth",
    "bills",
    "rewards",
    "accounts",
    "insights",
    "alerts",
    "export"
]