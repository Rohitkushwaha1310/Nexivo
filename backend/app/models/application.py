from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String, nullable=False)
    job_role = Column(String, nullable=False)
    
    status = Column(String, default="Applied")
    date_applied = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)

   
    user = relationship("User", back_populates="applications")
    interview_rounds = relationship("InterviewRound", back_populates="application")
    weak_areas = relationship("WeakArea", back_populates="application")
