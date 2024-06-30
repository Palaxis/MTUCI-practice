import React, { useState } from 'react';


const VacancyForm = ({ onSearch, onSimilarSearch, getAllVacancies, setminimalSalary, minimalSalary, setmaximalSalary, maximalSalary}) => {
  const [name, setName] = useState('');


  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(name);
  };

  const handleSetMinimal = (event) => {
    setminimalSalary(event.target.value);
    console.log(`minimal salary now is ${minimalSalary}`)
  }
  const handleSetMaximal = (event) => {
    setmaximalSalary(event.target.value);
    console.log(`maximal salary now is ${maximalSalary}`)
  }

  return (
    <div className="vacancy-form">
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Job Title:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <button type="submit">Search exact name</button>
      </form>
      <button onClick={() => onSimilarSearch(name)}>Search by similar name</button>
      <button onClick={() => getAllVacancies()}>Get all vacancies</button>
      <div>
        <input placeholder='minila salary' onChange={handleSetMinimal} ></input>
        <input placeholder='maximal salary'onChange={handleSetMaximal}></input>
      </div>
    </div>
  );
};

export default VacancyForm;
