import './DynamicCheckbox.css';
import React, { useState } from 'react';
import Card from '../UI/Card';

function DynamicCheckbox() {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const options = ["option1", "option2", "option3", "option4"];

  const toggleOption = (option) => {
    if (selectedOptions.includes(option)) {
      setSelectedOptions(selectedOptions.filter((item) => item !== option));
    } else {
      setSelectedOptions([...selectedOptions, option]);
    }
  };

  return (
    <div>
      <Card className="dropdown">
        <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
          {options.map((option) => (
            <label className="dropdown-item" key={option}>
              <input
                type="checkbox"
                checked={selectedOptions.includes(option)}
                onChange={() => toggleOption(option)}
              />{" "}
              {option}
            </label>
          ))}
        </div>
      </Card>
      <p>Selected options: {selectedOptions.join(', ')}</p>
    </div>
  );
}

export default DynamicCheckbox;