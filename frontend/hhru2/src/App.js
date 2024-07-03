import React, { useState } from 'react';
import axios from 'axios';
import VacancyForm from './components/VacancyForm';
import VacancyList from './components/VacancyList';
import './App.css';

const App = () => {
  const [vacancies, setVacancies] = useState([]);
  const [renderTrigger, setrenderTrigger] = useState(1);

  const [minimalSalary, setminimalSalary] = useState(0);
  const [maximalSalary, setmaximalSalary] = useState(10000000);

  const[amount, setAmount] = useState(10);
  const[area, setArea] = useState();
  const[employment, setEmployment] = useState();
  const[experience, setExperience] = useState();

  const getAllVacanciesBySalary = async () => {
    let salary_from = parseFloat(minimalSalary);
      let salary_to = parseFloat(maximalSalary);
    try {
      const response = await axios.get(`http://localhost:8000/get_all_vacancies_by_salary/`, { 
        params: {salary_from, salary_to},
      });
      setVacancies(response.data);
    } catch (error) {
      console.error('Error fetching vacancies:', error);
      setVacancies([]);
    }
  }
  

  const handleExactNameSearch = async (name) => {
    try {
      const response = await axios.get(`http://localhost:8000/exact_name_vacancies/`, {
        params: { name }
      });
      setVacancies(response.data);
    } catch (error) {
      console.error('Error fetching vacancies:', error);
      setVacancies([]);
    }
  };
  
  const handleSimilarSearch = async (name) => {
    try {
      const response = await axios.get(`http://localhost:8000/similar_name_vacancies/`, {
        params: { name },
      });
      setVacancies(response.data);
    } catch (error) {
      console.error('Error fetching vacancies:', error);
      setVacancies([]);
    }
  };

  const handleFilterParse = async (name) => {
    let page = Math.floor(amount/100);
    let per_page = amount % 100;
    try {
      const response = await axios.post(`http://localhost:8000/filter_parse-vacancies/`, null,{
        params: { text: name, per_page: per_page, page: page, area: area, employment: employment, experience: experience},
      });
      setVacancies(response.data);
    } catch (error) {
      console.error('Error fetching vacancies:', error);
      setVacancies([]);
    }
  };

  const deleteVacancy = (vacancy_id, valueToRemove) =>{    
    try{
      axios.delete(`http://localhost:8000/delete_vacancy/`, {params: {vacancy_id}})
      setVacancies(vacancies.filter(item => item !== valueToRemove))
      setrenderTrigger(renderTrigger+1);
    }
    catch(err){
      console.error('Error deleting item:', err);
    }

  }


  return (
    <div className="app-container">
      <div className="search-section">
        <VacancyForm onSearch={handleExactNameSearch} onSimilarSearch = {handleSimilarSearch} getAllVacancies={getAllVacanciesBySalary} setminimalSalary={setminimalSalary} minimalSalary={minimalSalary}
        setmaximalSalary={setmaximalSalary} maximalSalary={maximalSalary} amount={amount} setAmount={setAmount} setArea={setArea} setEmployment={setEmployment} setExperience={setExperience}
        handleFilterParse={handleFilterParse}/>
      </div>
      <div className="results-section">
        <VacancyList vacancies={vacancies} deleteVacancy={deleteVacancy} renderTrigger={renderTrigger}/>
      </div>
    </div>
  );
};

export default App;
