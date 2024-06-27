from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    salary_from = Column(Float, nullable=True)
    salary_to = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    city = Column(String)
    street = Column(String, nullable=True)
    building = Column(String, nullable=True)
    employer_name = Column(String)
    published_at = Column(DateTime)
    created_at = Column(DateTime)
    url = Column(String)
    requirement = Column(String, nullable=True)
    responsibility = Column(String, nullable=True)
