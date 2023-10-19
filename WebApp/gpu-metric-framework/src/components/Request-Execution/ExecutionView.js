import React, {useState } from 'react';

import './ExecutionView.css';
import DynamicCheckbox from './DynamicCheckbox';
import Card from '../UI/Card';
import StaticCheckbox from './StaticCheckbox';
import Dropdown from './Dropdown';
import TextInput from './TextInput';


function ExecutionView(props) { 
    const freqString= 'Please enter a frequency between 800GHz and 1100GHz.';
    const blockString= 'Please enter the amout of blocks per grid. The max is 2147483647.';
    const threadString= 'Please enter the amount of threads per block. The max is 1024.';
    const apps = 'apps';
    const workloads = 'workloads';
    const freq='freq';
    const blocks='blocks';
    const threads='threads';
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
                <div>
                    <label className='label'>Select the applications</label>
                    <DynamicCheckbox itemsURL={props.appsURL} field={apps} onExecuteEvent = {executeHandler} ></DynamicCheckbox>
                </div>
                <div>
                    <label className='label'>Select the workloads</label>
                    <DynamicCheckbox itemsURL={props.workloadsURL} field={workloads} onExecuteEvent = {executeHandler}></DynamicCheckbox>
                </div>
                <div>
                    <div>
                        <label className='label'>Sele ct the execution mode</label>
                    </div>
                    <StaticCheckbox onExecuteEvent = {executeHandler}></StaticCheckbox>
                </div>
                <div>
                 <label className='label'>Amount of executions</label>
                 <Dropdown onExecuteEvent = {executeHandler}></Dropdown>
                </div>
                
            </Card>
            <Card className='right-container'>
                
                <div>
                    <label className='label'>Select the GPU frequency</label>
                    <TextInput field={freq} onExecuteEvent = {executeHandler} label={freqString}></TextInput>
                </div>
                <div>
                    <label className='label'>Amount of blocks</label>
                    <TextInput field={blocks} onExecuteEvent = {executeHandler} label={blockString}></TextInput>
                </div>
                <div>
                    <label className='label'>Amount of threads</label>
                    <TextInput field={threads} onExecuteEvent = {executeHandler} label={threadString}></TextInput>
                </div>
                <button className='button' onClick={requestExecution}>Execute</button>
            </Card>
        </div>
    );
}

export default ExecutionView;