import './DynamicCheckbox.css';
import React, { useState, useEffect  } from 'react';
import Card from '../UI/Card';

function DynamicCheckbox(props) {

  const [selectedOption, setSelectedOption] = useState([]);
  const [appsOptions, setAppsOptions] = useState(null);
  const [error, setError] = useState(null);

  //Function to fetch data from the api
  //The item will depend on the props, it could be for the workloads or the apps data.
  useEffect(() => {
    setError(null);
    fetch(props.itemsURL ,{
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          'ngrok-skip-browser-warning': '1'
      }
  })
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
      setError(error.message);
    });
  }, []);
  

  //This function retrieves the data to the parent(ExecutionView) throught the function props.onExecuteEvent
  //This function gets triggered every time after the page renders
  useEffect(() => {
    // This code will run after the render

    if(props.refresh == true){
      setSelectedOption(null);
    }
    
    if (props.appName === 'BFS' && selectedOption !== null) {
      const bfs_workload = {
        bfs_workload: selectedOption
      };
      props.onExecuteEvent(bfs_workload);
    } else if (props.appName === 'Gauss' && selectedOption !== null) {
      const gauss_workload = {
        gauss_workload: selectedOption
      };
      props.onExecuteEvent(gauss_workload);
    }
  }, [props.refresh ,selectedOption]);

    
  // Function to update the selected option
  const toggleOption = (option) => {
    if (selectedOption === option) {
      // Deselect the option if it's already selected
      setSelectedOption(null);
    } else {
      // Select the new option
      setSelectedOption(option);
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
                className='options-style'
                checked={selectedOption === option}
                onChange={() => toggleOption(option)}
              />{" "}
              {option}
            </label>
          ))}
        </div>
      </Card>
      {error != null && <label className='warning'>Error: {error}</label>}
      

    </div>
  );
}

export default DynamicCheckbox;