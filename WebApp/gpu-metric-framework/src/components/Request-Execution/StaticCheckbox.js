import './StaticCheckbox.css';
import React, {useState, useEffect} from 'react';

const StaticCheckbox = (props) =>{

    const [executionFlag, setExecutionFlag] = useState(false);

    const handleCheckboxChange = (event) =>{
        const id = event.target.id;

        // If the clicked checkbox is already checked, uncheck it
        if (id === executionFlag) {
        setExecutionFlag(null);
        } else {
        setExecutionFlag(id); // Otherwise, check the clicked checkbox
        }
    }

    useEffect(() => {
        // This code will run after the state has been updated
        const executionType={ 
          execType: executionFlag
        };
        props.onExecuteEvent(executionType);  
        }, [executionFlag]);

    return(
        <div>
            <div className='checkbox-margin'>
                <label  className='form-control'>
                    <input
                        id='simult'
                        type='checkbox'
                        checked= {executionFlag === 'simult'}
                        onChange={handleCheckboxChange}
                    />Simultaneous
                </label> 
                <label className='form-control'>
                    <input
                        id='not-simult'
                        type='checkbox'
                        checked={executionFlag === 'not-simult'}
                        onChange={handleCheckboxChange}
                    />Not Simultaneous
                </label> 
            </div>
        </div>
        
    );
}

export default StaticCheckbox;