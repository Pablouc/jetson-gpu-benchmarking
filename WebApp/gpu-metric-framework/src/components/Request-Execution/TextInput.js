
import React, {useState, useEffect} from 'react';

import './TextInput.css';

const TextInput = (props) => {
    const [inputValue, setInputValue] = useState('');
    const [selectedNumber, setSelectedNumber] = useState(null);
  
    const handleInputChange = (event) => {
      const value = event.target.value;
      setInputValue(value);
  
      // Validate the input to ensure it's a number between 800 and 1100
      if (/^[8-9]\d{2}$|^10[0-9]{2}$|^1100$/.test(value)) {
        setSelectedNumber(parseInt(value, 10));
      } else {
        setSelectedNumber(null);
      }
    };

    //Sending data the the parent
    useEffect(() => {
      // This code will run after the state has been updated
  
      if(props.field=='freq'){
        const freq={ 
          freq:inputValue
        };
        props.onExecuteEvent(freq); 
      }

      if(props.field=='threads'){
        const threads={ 
          threads:inputValue
        };
        props.onExecuteEvent(threads); 
      }
      
      else if(props.field=='blocks'){
        const blocks={ 
          blocks:inputValue
        };
        props.onExecuteEvent(blocks); 
      } 
      }, [inputValue]);


  
    return (
      <div>
        <label>{props.label}</label>
        <div>
          <input className='text-box'
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Enter a number"
          />
        </div>
      </div>
    );
}

export default TextInput;