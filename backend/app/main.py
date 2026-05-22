from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import Base, engine
from app.models import user, application, interview_round, weak_area
from app.routes import user_routes, application_routes, interview_routes, dashboard_routes
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Nexivo",
    description="Backend API for tracking interview applications and progress",
    version="1.0.0"
)

# allow frontend talk backebd 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-site-name.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes
app.include_router(user_routes.router)
app.include_router(application_routes.router)
app.include_router(interview_routes.router)
app.include_router(dashboard_routes.router)


@app.get("/")
def root():
    return {"message": "Nexivo API is running!"}