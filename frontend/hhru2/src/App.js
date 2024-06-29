import React, { useState } from 'react';
import axios from 'axios';
import VacancyForm from './components/VacancyForm';
import VacancyList from './components/VacancyList';
import './App.css';

const App = () => {
  const [vacancies, setVacancies] = useState([]);

  const handleSearch = async (name) => {
    try {
      const response = await axios.get(`http://localhost:8000/vacancies/`, {
        params: { name },
      });
      setVacancies(response.data);
    } catch (error) {
      console.error('Error fetching vacancies:', error);
    }
  };

  return (
    <div className="app-container">
      <div className="search-section">
        <VacancyForm onSearch={handleSearch} />
      </div>
      <div className="results-section">
        <VacancyList vacancies={vacancies} />
      </div>
    </div>
  );
};

export default App;
