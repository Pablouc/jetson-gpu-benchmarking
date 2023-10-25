import React, {useState } from 'react';

import './ExecutionView.css';
import DynamicCheckbox from './DynamicCheckbox';
import Card from '../UI/Card';
import StaticCheckbox from './StaticCheckbox';
import Dropdown from './Dropdown';
import TextInput from './TextInput';
import AppComponent from '../Apps/AppComponent';

function ExecutionView(props) { 
    const freqString= 'Please enter a frequency between 800GHz and 1100GHz.';
    const workloads = 'workloads';
    const freq='freq';
    let userData = {};

    const [refreshFlag, setRefreshFlag] = useState(false);

    const executeHandler = ( enteredUserData ) => {
        userData = {
            ...userData, // Keep the existing data in userData
            ...enteredUserData, // Add the data from enteredUserData
          };
        
             
    }




    async function requestExecution(){
        setRefreshFlag(true);
        const response = await fetch(props.executionURL, {
            method: 'POST',
            body: JSON.stringify(userData),
            headers:{
                "Content-Type": "application/json"
            }
           
        });
        const data = await response.json();

        setRefreshFlag(false);
        console.log(data);
        
    }

    return(
        <div className='container'>
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
                    <AppComponent itemsURL={props.bfs_workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'BFS'}/>
                </div>

                <div>
                    <AppComponent itemsURL={props.cfd_workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'CFD'}/>
                </div>

                <div>
                    <AppComponent itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'Srad'}/>
                </div>

                <div>
                    <AppComponent itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'Particle Filter'}/>
                </div>

               
                
            </Card>
            <Card className='right-container'>

                 <div className='margins'>
                    <AppComponent itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'LavaMD'}/>
                </div>

                <div>
                    <AppComponent itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler} appName  ={'Lud'}/>
                </div>

                <div>
                    <div>
                        <label className='label'>Select the execution mode</label>
                    </div>
                    <StaticCheckbox onExecuteEvent = {executeHandler}></StaticCheckbox>
                </div>

                <div>
                 <label className='label'>Amount of executions</label>
                 <Dropdown onExecuteEvent = {executeHandler}></Dropdown>
                </div>
                
                <div>
                    <label className='label'>Select the GPU frequency</label>
                    <TextInput field={freq} onExecuteEvent = {executeHandler} label={freqString}></TextInput>
                </div>
                <button className='button' onClick={requestExecution}>Execute</button>
            </Card>
        </div>
    );
}

export default ExecutionView;