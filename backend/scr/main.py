from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

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

engine = create_engine('sqlite:///vacancies.db')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def extract_fields(vacancy):
    return {
        'id': vacancy['id'],
        'name': vacancy['name'],
        'salary_from': vacancy['salary']['from'] if vacancy.get('salary') else None,
        'salary_to': vacancy['salary']['to'] if vacancy.get('salary') else None,
        'currency': vacancy['salary']['currency'] if vacancy.get('salary') else None,
        'city': vacancy['address']['city'] if vacancy.get('address') else None,
        'street': vacancy['address']['street'] if vacancy.get('address') else None,
        'building': vacancy['address']['building'] if vacancy.get('address') else None,
        'employer_name': vacancy['employer']['name'],
        'published_at': datetime.fromisoformat(vacancy['published_at'].replace('Z', '+00:00')),
        'created_at': datetime.fromisoformat(vacancy['created_at'].replace('Z', '+00:00')),
        'url': vacancy['url'],
        'requirement': vacancy['snippet']['requirement'] if vacancy.get('snippet') else None,
        'responsibility': vacancy['snippet']['responsibility'] if vacancy.get('snippet') else None,
    }

def save_vacancies_to_db(vacancies, db: Session):
    for item in vacancies:
        fields = extract_fields(item)
        vacancy = Vacancy(**fields)
        db.merge(vacancy)
    db.commit()

def get_all_vacancies(db: Session):
    return db.query(Vacancy).all()

class VacancyQuery(BaseModel):
    query: str

@app.post("/parse-vacancies/")
def parse_vacancies(vacancy_query: VacancyQuery, db: Session = Depends(get_db)):
    url = f"https://api.hh.ru/vacancies?text={vacancy_query.query}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API")
    
    data = response.json()
    
    if 'items' in data:
        save_vacancies_to_db(data['items'], db)
    else:
        raise HTTPException(status_code=400, detail="Invalid data format received from API")
    
    vacancies = get_all_vacancies(db)

    for vacancy in vacancies:
        print(f"ID: {vacancy.id}, Name: {vacancy.name}, Salary_from: {vacancy.salary_from}")

    return {"message": "Parsed and saved successfully"}
