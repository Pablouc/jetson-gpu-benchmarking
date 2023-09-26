import React, { useState } from 'react';

import './Dropdown.css';

const Dropdown = () => {

    const [selectedNumber, setSelectedNumber] = useState(null);

    const handleSelectChange = (e) => {
      setSelectedNumber(e.target.value);
    };
  
    const numbers = Array.from({ length: 15 }, (_, i) => i + 1);
  
    return (
      <div>
        <select className='select' onChange={handleSelectChange} value={selectedNumber}>
          <option value="">Select a number</option>
          {numbers.map((number) => (
            <option key={number} value={number}>
              {number}
            </option>
          ))}
        </select>
      </div>
    );
}


export default Dropdown;