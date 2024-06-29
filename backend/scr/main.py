from fastapi import FastAPI, HTTPException, Depends 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import requests 
from datetime import datetime 
from pydantic import BaseModel

from database import engine, get_db, Base
from models import Vacancy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание всех таблиц
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def extract_fields(vacancy): 
    return { 
        'id': int(vacancy['id']), 
        'name': vacancy['name'], 
        'salary_from': vacancy['salary']['from'] if vacancy.get('salary') else None, 
        'salary_to': vacancy['salary']['to'] if vacancy.get('salary') else None, 
        'currency': vacancy['salary']['currency'] if vacancy.get('salary') else None, 
        'city': vacancy['address']['city'] if vacancy.get('address') else None, 
        'street': vacancy['address']['street'] if vacancy.get('address') else None, 
        'building': vacancy['address']['building'] if vacancy.get('address') else None, 
        'employer_name': vacancy['employer']['name'], 
        # 'published_at': datetime.fromisoformat(vacancy['published_at'].replace('Z', '+00:00')),
        
        # 'created_at': datetime.fromisoformat(vacancy['created_at'].replace('Z', '+00:00')), 
        'url': vacancy['url'], 
        'requirement': vacancy['snippet']['requirement'] if vacancy.get('snippet') else None, 
        'responsibility': vacancy['snippet']['responsibility'] if vacancy.get('snippet') else None, 
    }

async def save_vacancies_to_db(vacancies, db: AsyncSession): 
    for item in vacancies: 
        fields = extract_fields(item) 
        # Распаковка словаря
        print(fields)
        vacancy = Vacancy(**fields)
        # Добавление vacancy в базу данных
        db.add(vacancy) 
    await db.commit()

async def get_all_vacancies(db: AsyncSession): 
    result = await db.execute(select(Vacancy))
    return result.scalars().all()

async def get_vacancies_by_name(name: str, db: AsyncSession):
    result = await db.execute(select(Vacancy).where(Vacancy.name == name))
    return result.scalars().all()

class VacancyQuery(BaseModel): 
    query: str

@app.post("/parse-vacancies/") 
async def parse_vacancies(vacancy_query: VacancyQuery, db: AsyncSession = Depends(get_db)): 
    url = f"https://api.hh.ru/vacancies?text={vacancy_query.query}" 
    response = requests.get(url) 

    if response.status_code != 200: 
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API") 

    data = response.json() 

    if 'items' in data: 
        await save_vacancies_to_db(data['items'], db) 
    else: 
        raise HTTPException(status_code=400, detail="Invalid data format received from API") 

    vacancies = await get_all_vacancies(db) 

    for vacancy in vacancies: 
        print(f"ID: {vacancy.id}, Name: {vacancy.name}, Salary_from: {vacancy.salary_from}") 

    # print('parsed data:')
    # print(data)
    return {"message": "Parsed and saved successfully"}

@app.get("/vacancies/")
async def fetch_vacancies(name: str, db: AsyncSession = Depends(get_db)):
    vacancies = await get_vacancies_by_name(name, db)
    if not vacancies:
        raise HTTPException(status_code=404, detail="Vacancies not found")
    return vacancies

