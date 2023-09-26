import React, { useState } from 'react';

import './ExecutionView.css';
import DynamicCheckbox from './DynamicCheckbox';
import Card from '../UI/Card';
import StaticCheckbox from './StaticCheckbox';
import Dropdown from './Dropdown';
import Frequency from './Frequency';

function ExecutionView(props) { 

    const executeHandler = () => {
        console.log("Coocking!!");
    }

    return(
        <div className='container'>
            <Card className='left-container'>
                <div>
                    <label className='label'>Select the applications</label>
                    <DynamicCheckbox></DynamicCheckbox>
                </div>
                <div>
                    <label className='label'>Select the workloads</label>
                    <DynamicCheckbox></DynamicCheckbox>
                </div>
                <div>
                    <div>
                        <label className='label'>Select the execution mode</label>
                    </div>
                    <StaticCheckbox></StaticCheckbox>
                </div>
                <div>
                 <label className='label'>Amount of executions</label>
                 <Dropdown></Dropdown>
                </div>
                
            </Card>
            <Card className='right-container'>
                
                <div>
                    <label className='label'>Select the GPU frequency</label>
                    <Frequency></Frequency>
                </div>
                <div>
                    <label className='label'>Amount of blocks</label>
                </div>
                <div>
                    <label className='label'>Amount of threads</label>
                </div>
                <button className='button' onClick={executeHandler}>Execute</button>
            </Card>
        </div>
    );
}

export default ExecutionView;