
import React, {useState} from 'react';

import './Frequency.css';

const Frequency = () => {
    const [inputValue, setInputValue] = useState('');
    const [selectedNumber, setSelectedNumber] = useState(null);
  
    const handleInputChange = (e) => {
      const value = e.target.value;
      setInputValue(value);
  
      // Validate the input to ensure it's a number between 800 and 1100
      if (/^[8-9]\d{2}$|^10[0-9]{2}$|^1100$/.test(value)) {
        setSelectedNumber(parseInt(value, 10));
      } else {
        setSelectedNumber(null);
      }
    };
  
    return (
      <div>
        <label>Please enter a frequency among 800GHz and 1100GHz</label>
        <input className='text-box'
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter a number"
        />

      </div>
    );
}

export default Frequency;