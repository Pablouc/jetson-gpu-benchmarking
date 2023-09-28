import './DynamicCheckbox.css';
import React, { useState, useEffect  } from 'react';
import Card from '../UI/Card';

function DynamicCheckbox(props) {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const options = ["option1", "option2", "option3", "option4"];

  const toggleOption = (option) => {
    if (selectedOptions.includes(option)) {
      setSelectedOptions(selectedOptions.filter((item) => item !== option));
      console.log(selectedOptions.join(', '));
    } else {
      setSelectedOptions([...selectedOptions, option]);
      console.log(selectedOptions.join(', '));
    }
    /*props.onExecuteHandler(selectedOptions.join(', '));*/
  };

  useEffect(() => {
    // This code will run after the state has been updated

    if(props.field=='apps'){
      const apps={ 
        apps:selectedOptions.join(', ')
      };
      props.onExecuteEvent(apps); 
    }
    
    else if(props.field=='workloads'){
      const workloads={ 
        workloads:selectedOptions.join(', ')
      };
      props.onExecuteEvent(workloads); 
    } 
    }, [selectedOptions]);

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