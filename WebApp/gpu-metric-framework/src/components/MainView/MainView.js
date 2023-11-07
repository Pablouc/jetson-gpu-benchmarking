import Navbar from "../UI/Navbar";
import ExecutionView from "../Request-Execution/ExecutionView";
import MonitoringView from "../Monitoring/MonitoringView";


import React, {useState } from 'react';


function MainView(props) {

    const [showMonitoring, setShowMonitoring] = useState(false);

    //Options: Succed, Failed, InProgress, Paused
    const [executingState, setExecutingState] = useState('Paused');

    const handleView = (viewFlag) =>{
        setShowMonitoring(viewFlag);
    }

    const handleExecState = (exec_state) =>{
        setExecutingState(exec_state);
        console.log(exec_state);
    }


    return (
      <div>
        <Navbar/>
        {
            showMonitoring == false  && (
                <>
                <ExecutionView cfd_workloadsURL={props.cfd_workloadsURL} bfs_workloadsURL={props.bfs_workloadsURL} 
                      executionURL={props.executionURL} frequenciesURL={props.frequenciesURL} setView={handleView} 
                      setExecState={handleExecState}/>
                </>
            ) 
        }
        {
            showMonitoring == true && (
                <> 
                <MonitoringView resultsFileURL={props.resultsFileURL} setView={handleView} currentAppsURL={props.currentAppsURL} 
                getExecState={executingState} gpu_dataURL={props.gpu_dataURL} gpu_IterDataURL= {props.gpu_IterDataURL}
                execTimeURL={props.execTimeURL}/>
                </>
            )
        }
        
      </div>
    );
  }
  
  export default MainView;