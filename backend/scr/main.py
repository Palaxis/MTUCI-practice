from fastapi import FastAPI, HTTPException, Depends 
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.sql import and_
import requests 
from datetime import datetime 
from pydantic import BaseModel
from typing import Optional

from scr.database import engine, get_db, Base
from scr.models import Vacancy

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
        'experience': vacancy['experience']['name'] if vacancy.get('experience') else None,
    }

async def save_vacancies_to_db(vacancies, db: AsyncSession):
    for item in vacancies:
        fields = extract_fields(item)
        print(fields)

        insert_stmt = pg_insert(Vacancy).values(**fields)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=['id'],  # Укажите ключевые столбцы для конфликта
            set_=fields  # Поля для обновления при конфликте
        )

        await db.execute(upsert_stmt)

    await db.commit()

# def prepare_parse_responce(vacancies):
#     responce = []
#     i = 0
#     for item in vacancies:
#         responce[i] = extract_fields(item)
#         i += 1
#     return responce


async def get_all_vacancies(db: AsyncSession): 
    result = await db.execute(select(Vacancy))
    return result.scalars().all()

async def get_all_vacancies_by_salary(minimal_salary: float, maximal_salary: float, db: AsyncSession): 
    result = await db.execute(select(Vacancy).where( and_(Vacancy.salary_from > minimal_salary, Vacancy.salary_to < maximal_salary)))
    return result.scalars().all()

async def get_vacancies_by_id(id: int, db: AsyncSession):
    result = await db.execute(select(Vacancy).where(Vacancy.id == id))
    return result.scalars().all()

async def get_vacancies_by_exact_name(name: str, db: AsyncSession):
    result = await db.execute(select(Vacancy).where(Vacancy.name == name))
    return result.scalars().all()

async def get_vacancies_by_similar_name(name: str, db: AsyncSession):
    result = await db.execute(select(Vacancy).where(Vacancy.name.ilike(f'%{name}%')))
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

    vacancies = data.get('items', []) 

    vaclen = len(vacancies)
    # for item in vacancies: 
    #     # print(f"ID: {item.id}, Name: {item.name}, Salary_from: {item.salary_from}") 
    #     vaclen += 1

    # print(vaclen)
    print(vacancies)
    return {"message": f'Parsed and saved successfully {vaclen} vacancies'}

@app.post("/filter_parse-vacancies") 
async def parse_vacancies(text: str, per_page: int, page: int,area: int = None, employment: str = None, experience: str = None, db: AsyncSession = Depends(get_db)): 
    url = f"https://api.hh.ru/vacancies?text={text}&per_page={per_page}&page={page}"

    if area:
        url += f"&area={area}"

    if employment:
        url += f"&employment={employment}"

    if experience:
        url += f"&experience={experience}"

    response = requests.get(url) 

    if response.status_code != 200: 
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API") 

    data = response.json() 

    if 'items' in data: 
        await save_vacancies_to_db(data['items'], db) 
    else: 
        raise HTTPException(status_code=400, detail="Invalid data format received from API") 

    vacancies = data.get('items', []) 

    vaclen = len(vacancies)
    # for item in vacancies: 
    #     # print(f"ID: {item.id}, Name: {item.name}, Salary_from: {item.salary_from}") 
    #     vaclen += 1

    # print(vaclen)
    # print(vacancies)
    
    # response = prepare_parse_responce(data['items'])

    formatted_vacancies = [extract_fields(item) for item in vacancies]
    return formatted_vacancies

@app.get("/get_all_vacancies/")
async def fetch_vacancies(db: AsyncSession = Depends(get_db)):
    vacancies = await get_all_vacancies(db)
    if not vacancies:
        raise HTTPException(status_code=404, detail="Vacancies not found")
    return vacancies

@app.get("/get_all_vacancies_by_salary/")
async def fetch_vacancies(salary_from: float, salary_to: float, db: AsyncSession = Depends(get_db)):
    vacancies = await get_all_vacancies_by_salary(salary_from, salary_to, db)
    if not vacancies:
        raise HTTPException(status_code=404, detail="Vacancies not found")
    return vacancies

@app.get("/exact_name_vacancies/")
async def fetch_vacancies(name: str, db: AsyncSession = Depends(get_db)):
    vacancies = await get_vacancies_by_exact_name(name, db)
    if not vacancies:
        raise HTTPException(status_code=404, detail="Vacancies not found")
    return vacancies

@app.get("/similar_name_vacancies/")
async def fetch_vacancies(name: str, db: AsyncSession = Depends(get_db)):
    vacancies = await get_vacancies_by_similar_name(name, db)
    if not vacancies:
        raise HTTPException(status_code=404, detail="Vacancies not found")
    return vacancies

@app.delete("/delete_vacancy/")
async def delete_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_db)):
    vacancy = await get_vacancies_by_id(vacancy_id, db)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy id not found")
    
    stmt = delete(Vacancy).where(Vacancy.id == vacancy_id)
    result = await db.execute(stmt)
    await db.commit()
    print(vacancy)
    return {"Detail": "Vacancy deleted"}

@app.delete("/drop_all_vacancies/")
async def delete_all_vacancies(db: AsyncSession = Depends(get_db)):
    stmt = delete(Vacancy)
    result = await db.execute(stmt)
    await db.commit()
    return {"Detail": "All vacancies deleted"}
