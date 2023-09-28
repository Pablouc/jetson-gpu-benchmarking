import './DynamicCheckbox.css';
import React, { useState, useEffect  } from 'react';
import Card from '../UI/Card';

function DynamicCheckbox(props) {

  const [selectedOptions, setSelectedOptions] = useState([]);
  const [appsOptions, setAppsOptions] = useState(null);

  //Function to fetch data from the api
  //The item will depend on the props, it could be for the workloads or the apps data.
  useEffect(() => {
    fetch(props.itemsURL)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      setAppsOptions(data.itemNames);
    })
    .catch((error) => {
      console.error('Fetch error:', error);
    });
  }, []); 
  

  //This function retrieves the data to the parent(ExecutionView) throught the function props.onExecuteEvent
  //This function gets triggered every time after the page renders
  useEffect(() => {
    // This code will run after the render
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

    
    //Function to update the list of items in the list that is going to be retrieved to the parent component.
    const toggleOption = (option) => {
      if (selectedOptions.includes(option)) {
        setSelectedOptions(selectedOptions.filter((item) => item !== option));
        console.log(selectedOptions.join(', '));
      } else {
        setSelectedOptions([...selectedOptions, option]);
        console.log(selectedOptions.join(', '));
      }
    };

  return (
    <div>
      <Card className="dropdown">
        <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
          {/* This validation -> appsOptions && is used to make sure that the map is executed util the variable appsOptions has been fetched.
              This is because fetch is an async function.*/}
          {appsOptions && appsOptions.map((option) => (
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