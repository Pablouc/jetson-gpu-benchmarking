import Navbar from "../UI/Navbar";
import ExecutionView from "../Request-Execution/ExecutionView";
import MonitoringView from "../Monitoring/MonitoringView";


import React, {useState } from 'react';


function MainView(props) {

    const [showMonitoring, setShowMonitoring] = useState(false);

    //Options: Succed, Failed, InProgress, Paused
    const [executingState, setExecutingState] = useState('Paused');
    const [executionType, setExecutionType] = useState('');
    const [executionsNumber, setExecutionsNumber] = useState(0)

    const handleView = (viewFlag) =>{
        setShowMonitoring(viewFlag);
    }

    const handleExecState = (exec_state) =>{
        setExecutingState(exec_state);
        console.log(exec_state);
    }

    const handleExecProperties = (exec_properties) =>{
        console.log(exec_properties);
        if(exec_properties[0] == 'not-simult'){setExecutionType('sequential')}
        else if(exec_properties[0] == 'simult'){setExecutionType('simultaneous')}
        setExecutionsNumber(exec_properties[1])
    }


    return (
      <div>
        <Navbar/>
        {
            showMonitoring == false  && (
                <>
                <ExecutionView cfd_workloadsURL={props.cfd_workloadsURL} bfs_workloadsURL={props.bfs_workloadsURL} 
                                executionURL={props.executionURL} frequenciesURL={props.frequenciesURL} setView={handleView} 
                                setExecState={handleExecState} setExecProperties={handleExecProperties}/>
                </>
            ) 
        }
        {
            showMonitoring == true && (
                <> 
                <MonitoringView resultsFileURL={props.resultsFileURL} setView={handleView} 
                                getExecState={executingState} gpu_dataURL={props.gpu_dataURL} 
                                execTimeURL={props.execTimeURL} execType ={executionType} execNum={executionsNumber}/>
                </>
            )
        }
        
      </div>
    );
  }
  
  export default MainView;