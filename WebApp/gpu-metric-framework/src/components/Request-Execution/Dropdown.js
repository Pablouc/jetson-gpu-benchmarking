import React, { useState, useEffect } from 'react';

import './Dropdown.css';

const Dropdown = (props) => {

    const [selectedNumber, setSelectedNumber] = useState('');

    const handleSelectChange = (e) => {
      setSelectedNumber(e.target.value);
    };
  
    const numbers = Array.from({ length: 15 }, (_, i) => i + 1);

    
    useEffect(() => {
      // This code will run after the state has been updated
      const execNum={ 
        execNum: selectedNumber
      };
      props.onExecuteEvent(execNum);  
      }, [selectedNumber]);
  
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