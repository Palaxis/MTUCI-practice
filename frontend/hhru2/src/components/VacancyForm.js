import React, { useState } from 'react';

const VacancyForm = ({ onSearch }) => {
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(name);
  };

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
        <button type="submit">Search</button>
      </form>
    </div>
  );
};

export default VacancyForm;
