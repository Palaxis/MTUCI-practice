from sqlalchemy import Column, Integer, String, Float, DateTime
from scr.database import Base

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    salary_from = Column(Float, nullable=True)
    salary_to = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)
    building = Column(String, nullable=True)
    employer_name = Column(String)
    # published_at = Column(DateTime)
    # created_at = Column(DateTime)
    url = Column(String)
    requirement = Column(String, nullable=True)
    responsibility = Column(String, nullable=True)
    experience = Column(String, nullable=True)

