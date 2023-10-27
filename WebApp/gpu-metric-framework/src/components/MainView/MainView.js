import Navbar from "../UI/Navbar";
import ExecutionView from "../Request-Execution/ExecutionView";
import MonitoringView from "../Monitoring/MonitoringView";


import React, {useState } from 'react';


function MainView(props) {

    const [showMonitoring, setShowMonitoring] = useState(false);

    const handleView = (viewFlag) =>{
        setShowMonitoring(viewFlag);
        console.log("no sirve");
        console.log(showMonitoring);
    }


    return (
      <div>
        <Navbar/>
        {
            showMonitoring == false  && (
                <>
                <ExecutionView cfd_workloadsURL={props.cfd_workloadsURL} bfs_workloadsURL={props.bfs_workloadsURL} 
                      executionURL={props.executionURL} frequenciesURL={props.frequenciesURL} setView={handleView}/>
                </>
            ) 
        }
        {
            showMonitoring == true && (
                <> 
                <MonitoringView resultsFileURL={props.resultsFileURL}/>
                </>
            )
        }
        
      </div>
    );
  }
  
  export default MainView;