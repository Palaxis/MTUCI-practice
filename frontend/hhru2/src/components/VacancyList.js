import React from 'react';

const VacancyList = ({ vacancies }) => {
  return (
    <div className="vacancy-list">
      {vacancies.length === 0 && <p>No vacancies found.</p>}
      {vacancies.map((vacancy) => (
        <div key={vacancy.id} className="vacancy-item">
          <h3>{vacancy.name}</h3>
          <p>{vacancy.employer_name}</p>
          {vacancy.salary_from && <p>From: {vacancy.salary_from}</p>}
          {vacancy.salary_to && <p>To: {vacancy.salary_to}</p>}
          <a href={vacancy.url} target="_blank" rel="noopener noreferrer">View Details</a>
        </div>
      ))}
    </div>
  );
};

export default VacancyList;
