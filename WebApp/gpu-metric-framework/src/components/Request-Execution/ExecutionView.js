import React, {useState, useEffect } from 'react';

import './ExecutionView.css';
import Card from '../UI/Card';
import StaticCheckbox from './StaticCheckbox';
import Dropdown from './Dropdown';
import AppComponent from '../Apps/AppComponent';
import Popup from '../UI/PopUp';

function ExecutionView(props) { 
    const workloads = 'workloads';
    let userData = {};

    const [refreshFlag, setRefreshFlag] = useState(false);
    const [isPopupOpen, setPopupOpen] = useState(false);
    const [MonitoringFlag, setMonitoringFlag] = useState(false);

    const executeHandler = ( enteredUserData ) => {
        userData = {
            ...userData, // Keep the existing data in userData
            ...enteredUserData, // Add the data from enteredUserData
          };
         
    }

    async function requestExecution() {
        setRefreshFlag(true);
        setRefreshFlag(false);
        setMonitoringFlag(true);
        props.setExecState('InProgress');
        props.setExecProperties([userData['execType'], userData['execNum']]);
        try {
          const response = await fetch(props.executionURL, {
            method: 'POST',
            body: JSON.stringify(userData),
            headers: {
              'Content-Type': 'application/json',
            },
          });
      
          if (!response.ok) {
            // Handle HTTP errors
            props.setExecState('Failed');
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
      
          const data = await response.json();
          props.setExecState('Succed');
      
          console.log(data);
      
        } catch (error) {
            props.setExecState('Failed');
            console.error('Error:', error.message);
      
        }
      }
      


    const closePopup = () => {
        setPopupOpen(false);
        setMonitoringFlag(true);
      };

      useEffect(() => {
        props.setView(MonitoringFlag);
    }, [MonitoringFlag]);



    return(
        <div >
            <div className='popup'>
                <Popup isOpen={isPopupOpen} onClose={closePopup}/>
            </div>
            <div className='execution-container'>
                <Card className='left-container'>
                    <label className='label'>Select the applications</label>
                    {/* <div>
                        
                        <DynamicCheckbox itemsURL={props.appsURL} field={apps} onExecuteEvent = {executeHandler} ></DynamicCheckbox>
                    </div>
                    <div>
                        <label className='label'>Select the workloads</label>
                        <DynamicCheckbox itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler}></DynamicCheckbox>
                    </div> */}
                    <div>
                        <AppComponent refresh={refreshFlag} itemsURL={props.bfs_workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'BFS'}/>
                    </div>

                    <div>
                        <AppComponent refresh={refreshFlag} itemsURL={props.gauss_workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'Gauss'}/>
                    </div>

                    <div>
                        <AppComponent refresh={refreshFlag} itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'Srad'}/>
                    </div>

                    <div>
                        <AppComponent refresh={refreshFlag} itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'Particle Filter'}/>
                    </div>

                
                    
                </Card>
                <Card className='right-container'>

                    <div className='margins'>
                        <AppComponent refresh={refreshFlag} itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'LavaMD'}/>
                    </div>

                    <div>
                        <AppComponent refresh={refreshFlag} itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'Lud'}/>
                    </div>

                    <div>
                        <AppComponent refresh={refreshFlag} itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'External'}/>
                    </div>

                    <div>
                        <div>
                            <label className='label'>Select the execution mode</label>
                        </div>
                        <StaticCheckbox refresh={refreshFlag} onExecuteEvent = {executeHandler}></StaticCheckbox>
                    </div>

                    <div>
                    <label className='label'>Executions number</label>
                    <Dropdown refresh={refreshFlag} injected={false} onExecuteEvent = {executeHandler}></Dropdown>
                    </div>

                    <div>
                    <label className='label'>Select the frequencies</label>
                    <Dropdown refresh={refreshFlag} injected={true} frequenciesURL={props.frequenciesURL} onExecuteEvent = {executeHandler}></Dropdown>
                    </div>
                    
                    {/*<div>
                        <label className='label'>Select the GPU frequency</label>
                        <TextInput field={freq} onExecuteEvent = {executeHandler} label={freqString}></TextInput>
                    </div>
                */}
                    <button className='button' onClick={requestExecution}>Execute</button>
                </Card>
            </div>
        </div>
    );
}

export default ExecutionView;