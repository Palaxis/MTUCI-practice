import React from 'react';
import "./VacancyList.css";

const VacancyList = ({ vacancies, deleteVacancy, renderTrigger }) => {
  return (
    <div className="vacancy-list">
        <h1>Search results in database for {}</h1>
      {vacancies.length === 0 && <p>No vacancies found.</p>}
      {vacancies.map((vacancy) => (
        <div key={vacancy.id} className="vacancy-item">
          <h3>{vacancy.name}</h3>
          <p>{vacancy.employer_name}</p>
          {vacancy.salary_from && <p>From: {vacancy.salary_from}</p>}
          {vacancy.salary_to && <p>To: {vacancy.salary_to}</p>}
          <a href={vacancy.url} target="_blank" rel="noopener noreferrer">View Details</a>
          <button onClick={() => deleteVacancy(vacancy.id, vacancy)}>Delete Vacancy</button>
          <button>{renderTrigger}</button>
        </div>
      ))}
    </div>
  );
};

export default VacancyList;
