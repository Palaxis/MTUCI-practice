from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from pydantic import BaseModel
from database import engine, get_db
from models import Base, Vacancy

# Создаем Pydantic модель для запросов
class VacancyQuery(BaseModel):
    query: str

# Создаем экземпляр FastAPI
app = FastAPI()

@app.post("/parse-vacancies/")
def parse_vacancies(vacancy_query: VacancyQuery, db: Session = Depends(get_db)):
    url = f"https://api.hh.ru/vacancies?text={vacancy_query.query}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API")
    
    data = response.json()
    print(data) 
   
    return {"message": "Parsed success"}

# Примеры для создания таблицы, если они еще не существуют
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

    