import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from app.database.database import SessionLocal
from app.services.collection_processor import process_due_collections
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import router as auth_router
from app.auth.auth_bearer import verify_token

from app.routes.waste_bin_routes import router as waste_bin_router
from app.routes.schedule_routes import router as schedule_router
from app.routes.record_routes import router as record_router
from app.routes.notification_routes import router as notification_router
from app.routes.report_routes import router as report_router
from app.routes.prediction_routes import router as prediction_router
from app.routes.optimization_routes import router as optimization_router
from app.routes.decision_routes import router as decision_router
from app.routes.monitoring_routes import router as monitoring_router
from app.routes.route_routes import router as route_router
from app.routes.ml_routes import router as ml_router
from app.routes.admin_routes import router as admin_router
from app.routes.evaluation_routes import router as evaluation_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.ai_report_routes import router as ai_report_router
from app.routes.system_config_routes import router as system_config_router
from app.routes.audit_routes import router as audit_router
from app.routes.health_routes import router as health_router
from app.routes.permission_routes import router as permission_router
from app.routes.password_routes import router as password_router

async def automatic_collection_processor():
    while True:
        db = SessionLocal()

        try:
            processed = process_due_collections(db)

            if processed:
                print(
                    f"Automatically processed collections: {processed}"
                )

        except Exception as e:
            print(
                f"Automatic collection processing error: {e}"
            )

        finally:
            db.close()

        # Check every 60 seconds
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(
        automatic_collection_processor()
    )

    try:
        yield
    finally:
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Smart Waste Management System",
    version="1.0.0",
    lifespan=lifespan
)

# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        # Local Vite development
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        # Production frontend
        # We will add your actual Vercel domain here
        # after deploying the frontend.
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# API ROUTES
# =========================================================

app.include_router(auth_router)
app.include_router(waste_bin_router)
app.include_router(schedule_router)
app.include_router(record_router)
app.include_router(notification_router)
app.include_router(report_router)
app.include_router(prediction_router)
app.include_router(optimization_router)
app.include_router(decision_router)
app.include_router(monitoring_router)
app.include_router(route_router)
app.include_router(ml_router)
app.include_router(admin_router)
app.include_router(evaluation_router)
app.include_router(dashboard_router)
app.include_router(ai_report_router)
app.include_router(system_config_router)
app.include_router(audit_router)
app.include_router(health_router)
app.include_router(permission_router)
app.include_router(password_router)


# =========================================================
# DASHBOARD
# =========================================================

@app.get("/dashboard")
def dashboard(user=Depends(verify_token)):
    return {
        "message": "Welcome to Smart Waste Management Dashboard",
        "logged_in_user": user
    }


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Smart Waste Management System API"
    }