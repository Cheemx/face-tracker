import uuid

from sqlalchemy import Column, DateTime, Integer, String, func

from app.db.database import Base

class ROI(Base):
    __tablename__ = "rois"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)