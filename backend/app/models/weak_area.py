from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base


class WeakArea(Base):
    __tablename__ = "weak_areas"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    topic = Column(String, nullable=False)        
    detected_from = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

   
    application = relationship("Application", back_populates="weak_areas")
