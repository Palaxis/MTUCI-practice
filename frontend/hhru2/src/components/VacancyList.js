import React from 'react';
import "./VacancyList.css";

const VacancyList = ({ vacancies, deleteVacancy, renderTrigger }) => {
  return (
    <div className="vacancy-list">
        <h1>Search results {}</h1>
      {vacancies.length === 0 && <p>No vacancies found.</p>}
      {vacancies.map((vacancy) => (
        <div key={vacancy.id} className="vacancy-item">
          <h3>{vacancy.name}</h3>
          <p>Employer: {vacancy.employer_name}</p>
          {vacancy.salary_from && <p>Salary From: {vacancy.salary_from} {vacancy.currency}</p>}
          {vacancy.salary_to && <p>Salary To: {vacancy.salary_to} {vacancy.currency}</p>}
          <p>Responsibility: {vacancy.responsibility}</p>
          <a href={vacancy.url} target="_blank" rel="noopener noreferrer">View Details</a>
          <button onClick={() => deleteVacancy(vacancy.id, vacancy)}>Delete Vacancy</button>
        </div>
      ))}
    </div>
  );
};

export default VacancyList;
