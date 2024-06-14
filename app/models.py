# app/models.py

from sqlalchemy import Column, Integer, String, Table
from app.database import Base

class CourseItem(Base):
    __tablename__ = "course_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String, nullable=True)
