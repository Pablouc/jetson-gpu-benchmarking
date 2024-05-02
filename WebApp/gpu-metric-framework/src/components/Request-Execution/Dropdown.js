import React, { useState, useEffect } from 'react';

import './Dropdown.css';

const Dropdown = (props) => {

    const [selectedNumber, setSelectedNumber] = useState('');
    const [error, setError] = useState(null);
    const [frequenciesOptions, setFrequenciesOptions] = useState('');
    const [selectedFrequency, setSelectedFrequency] = useState('');

    const handleSelectChange = (e) => {
      setSelectedNumber(e.target.value);
    };
  
    const numbers = Array.from({ length: 1000 }, (_, i) => i);


    useEffect(() => {
      if (props.injected === true) {
        setError(null);
        fetch(props.frequenciesURL, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': '1',
          },
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            setFrequenciesOptions(data);
          })
          .catch((error) => {
            setError(error.message);
          });
      }
    }, [props.injected, props.frequenciesURL, props.frequenciesOptions]);

    
    useEffect(() => {
      // This code will run after the state has been updated
      if( props.refresh === true){
        setSelectedNumber('');
        setSelectedFrequency('');
      }

      if(props.injected== false){
        const execNum={ 
          execNum: selectedNumber
        };
        props.onExecuteEvent(execNum); 
      }
      
      if(props.injected== true){
        
        if(props.wickedApp == true){
          
          if(props.freq_boundary == 'min'){
            const wicked_minfreq={
              wicked_minfreq: selectedFrequency
            }
            props.onExecuteEvent(wicked_minfreq);
          }
          else{
            const wicked_maxfreq={
              wicked_maxfreq: selectedFrequency
          }
          props.onExecuteEvent(wicked_maxfreq);
          }
        
        }
        else{
          const freq={ 
            freq:selectedFrequency
          };
  
          props.onExecuteEvent(freq); 
        }
      }

      }, [props.refresh ,selectedFrequency,selectedNumber]);

  
    return (
      <div>
        {(props.injected == false) && (
          <div>
          {/*<select className='select' onChange={handleSelectChange} value={selectedNumber}>
            <option value=""></option>
             {numbers.map((number) => (
              <option key={number} value={number}>
                {number}
              </option>
            ))} 
            </select>*/}
            <input type="number" className='select' onChange={handleSelectChange} value={selectedNumber}/>
          

          </div>
        )}

        {(props.injected == true) && frequenciesOptions && (          
            <div>
            <select
              className="select"
              onChange={(e) => setSelectedFrequency(e.target.value)}
              value={selectedFrequency}
            >
              <option value="">Select a frequency</option>
              {frequenciesOptions.map((frequency) => (
                <option key={frequency} value={frequency}>
                  {frequency}
                </option>
              ))}
            </select>
          </div>
        )}
        
      </div>
    );
}


export default Dropdown;