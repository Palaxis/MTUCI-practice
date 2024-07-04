import React, { useState } from "react";
import "./VacancyForm.css";

const VacancyForm = ({
  onSearch,
  onSimilarSearch,
  getAllVacancies,
  setminimalSalary,
  minimalSalary,
  setmaximalSalary,
  maximalSalary,
  amount,
  setAmount,
  setArea,
  setEmployment,
  setExperience,
  handleFilterParse,
  filterSearch,
  onMagicParse
}) => {
  const [name, setName] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(name);
  };

  const handleSetMinimal = (event) => {
    setminimalSalary(event.target.value);
    console.log(`minimal salary now is ${minimalSalary}`);
  };
  const handleSetMaximal = (event) => {
    setmaximalSalary(event.target.value);
    console.log(`maximal salary now is ${maximalSalary}`);
  };

  return (
    <div>
      <div className="vacancy-form">
      <h4>Request vacancies from database</h4>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Job Title:</label>
          <input
            type="text"
            id="name"
            value={name}
            className="inputs"
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <button type="submit">Search exact name</button>
      </form>
      <button onClick={() => onSimilarSearch(name)}>
        Search by similar name
      </button>
      <button onClick={() => getAllVacancies()}>Get all vacancies</button>
      <p>Little filter down here:</p>
      <div className="minMaxSelect">
        <div> <p>minimal salary</p><input placeholder="minimal salary" className="inputs" onChange={handleSetMinimal}></input></div>
        
        <div> <p>maximal salary</p><input placeholder="maximal salary" className="inputs" onChange={handleSetMaximal}></input></div>
        
      </div>
      <div className="employmentSelect">
        <input
            type="radio"
            name="radio2"
            value="value1"
            onChange={() => setEmployment("Full")}
          />
          <label>Полная</label>
          <input
            type="radio"
            name="radio2"
            value="value2"
            onChange={() => setEmployment("Part")}
          />
          <label>Частичная</label>
          <input
            type="radio"
            name="radio2"
            value="value2"
            defaultChecked={true}
            onChange={() => setEmployment(null)}
          />
          <label>Не важно</label>
        </div>

        {/* Да, я использовал одинаковый выбор занятости в двух формах, и использовал для двух них один и тот же хук, чтобы не плодить лишние переменные */}
        <button onClick={() => filterSearch(name)}>Filter search</button>
      </div>
      <div className="parseDiv">
        <h4>Parse request to hh.ru:</h4>
        <input
          type="text"
          id="name"
          value={name}
          placeholder="Search request"
          className="inputs"
          onChange={(e) => setName(e.target.value)}
        />
        <br></br>
        <h5>Enter amount of vacancies:</h5>
        <input
          type="text"
          id="amount"
          value={amount}
          className="inputs"
          placeholder="amount (default = 10)"
          onChange={(e) => setAmount(e.target.value)}
        />
        <h5>Select area</h5>
        <div className="areaSelect">
          <input
            type="radio"
            name="radio1"
            value="value1"
            onChange={() => setArea(1)}
          />
          <label>Москва</label>
          <input
            type="radio"
            name="radio1"
            value="value2"
            onChange={() => setArea(2)}
          />
          <label>Санкт Петербург</label>
          <input
            type="radio"
            name="radio1"
            value="value2"
            defaultChecked={true}
            onChange={() => setArea(null)}
          />
          <label>Не важно</label>
        </div>
        <h5>Select employment</h5>
        <div className="employmentSelect">
        <input
            type="radio"
            name="radio2"
            value="value1"
            onChange={() => setEmployment("Full")}
          />
          <label>Полная</label>
          <input
            type="radio"
            name="radio2"
            value="value2"
            onChange={() => setEmployment("Part")}
          />
          <label>Частичная</label>
          <input
            type="radio"
            name="radio2"
            value="value2"
            defaultChecked={true}
            onChange={() => setEmployment(null)}
          />
          <label>Не важно</label>
        </div>
        <h5>Select experience</h5>
        <div className="experienceSelect">
        <input
            type="radio"
            name="radio3"
            value="value1"
            onChange={() => setExperience("noExperience")}
          />
          <label>Без опыта</label>
          <input
            type="radio"
            name="radio3"
            value="value2"
            onChange={() => setExperience("between1And3")}
          />
          <label>От 1 до 3 лет</label>
          <input
            type="radio"
            name="radio3"
            value="value2"
            onChange={() => setExperience("between3And6")}
          />
          <label>От 3 до 6 лет</label>
          <input
            type="radio"
            name="radio3"
            value="value2"
            onChange={() => setExperience("above6")}
          />
          <label>Более 6 лет</label>

          <input
            type="radio"
            name="radio3"
            value="value2"
            defaultChecked={true}
            onChange={() => setExperience(null)}
          />
          <label>Не важно</label>
        </div>
      <button onClick={() => handleFilterParse(name)}>Parse vacancies</button>

      {/* <button onClick={() => onMagicParse(name)}>
        Magic parse
      </button> */}

      </div>
      <button className="dropButton">DROP TABLE</button>
    </div>
  );
};

export default VacancyForm;
