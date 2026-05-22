from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base


class InterviewRound(Base):
    __tablename__ = "interview_rounds"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    round_name = Column(String, nullable=False)   
    feedback = Column(String, nullable=True)       
    
    result = Column(String, default="Pending")
    interview_date = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="interview_rounds")
