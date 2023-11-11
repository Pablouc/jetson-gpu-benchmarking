import { useState, useEffect, useRef } from "react";
import './MonitoringView.css';
import MyChart from "./MyChart";
import ExecutionTime from "./ExecutionTime";

function MonitoringView (props) {
  

    const [error, setError] = useState('');
    const [currentApps, setCurrentApps] = useState([]);
    const [gpuTemp, setGpuTemp] =  useState('');
    const [gpuFreq, setGpuFreq] =  useState('');
    const [gpuPower, setPower] =  useState('');
    const [gpu_PowerArray, setGpuPowerArray] = useState([]);
    const [gpu_TempArray, setGpuTempArray] = useState([]);
    const [gpu_ramArray, setGpuRamArray] = useState([]);
    const [timer, setTimer] = useState(0);
    const [execTimeArray, setExecTimeArray] = useState([]);
    const [iterationsTime, setIterationsTime] = useState([]);

    const tempChartRef = useRef(null);
    const powerChartRef = useRef(null);
    const ramChartRef = useRef(null);

    const downloadResults = () => {
        console.log(props.resultsFileURL);
        fetch(props.resultsFileURL, {
            method: 'GET',
            headers: {
                'ngrok-skip-browser-warning': '1'
            }
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.blob();
        })
        .then((blob) => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'execution_results.csv'; // Or whatever you want the filename to be
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch((error) => {
            setError(error.message);
        });
    }


    const fetch_GPUData = () => {
      setError(null);
      fetch(props.gpu_dataURL, {
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
          console.log(data);
          if(data != 'out of execution'){
            setGpuTemp(data.global_gpu_data.temperature);
            setGpuFreq(data.global_gpu_data.frequency);
            setPower(data.global_gpu_data.power);
            setGpuTempArray(data.gpu_iterations_data.temperature.map((temp) => parseFloat(temp)));
            setGpuPowerArray(data.gpu_iterations_data.power.map((temp) => parseFloat(temp)));
            setExecTimeArray(data.gpu_iterations_data.current_time);
            setIterationsTime(data.gpu_iterations_data.iteration_time);
            console.log(data.gpu_iterations_data.ram_used);
            setGpuRamArray(data.gpu_iterations_data.ram_used);
            let current_apps = data.global_current_apps;
            if (current_apps != ""){
              setCurrentApps(current_apps);
            }
            
            
          }
          
        })
        .catch((error) => {
          setError(error.message);
        });
    };




    useEffect(() => {
        if (props.getExecState === 'InProgress') {
          //fetch_AppsInUse();
          fetch_GPUData();
          //fetch_GPUIterationsData();
      
          // Set up a polling interval (every second in this example) for both
          const pollingIntervalId = setInterval(() => {
            //fetch_AppsInUse();
            fetch_GPUData();
            //fetch_GPUIterationsData();
          }, 1000);
      
            return () => clearInterval(pollingIntervalId);
        }
        else{setCurrentApps([])}
    }, [props.currentAppsURL, currentApps, props.getExecState, props.gpuData]);

  
    useEffect(() => {
      if (props.getExecState === 'InProgress'){
        const interval = setInterval(() => {
          // Update the timer every second (1000 milliseconds)
          setTimer((prevTimer) => prevTimer + 100);
        }, 100);
    
        // Cleanup the interval when the component unmounts
        return () => clearInterval(interval);
      }
    }, [props.getExecState]);


    const changeView=()=>{
      setGpuTemp('');
      setGpuFreq('');  
      setPower('');  
      setGpuPowerArray ([]);
      setGpuTempArray([]);
      setExecTimeArray([]);
      setIterationsTime([]);
      props.setView(false);
    }


    return(
        <div>
        
            <div>
              <div>
                <button className="monitoring-button" onClick={downloadResults}>Download results</button>
                <button className="monitoring-button" onClick={changeView}>Request Execution</button>
              </div>
              <div>
                <label className="execution-time">Execution time: {timer/1000} s</label>
              </div>
          
            </div>
            <div className="container">

                <div className="cell"> 
                  <div className="cell-Title">
                    <h2 >Apps being executed </h2>
                  </div>
                  <div className="cell-body">
                      {currentApps === null ? (
                          <p>Loading...</p>
                      ) : Array.isArray(currentApps) ? (
                          currentApps.map((item, index) => (
                              <div key={index} className="boldText">
                                <div>{item}</div>
                              </div>
                          ))
                      ) : (
                          <p>currentApps is not an array</p>
                      )}
                  </div>
                </div>
                
                <div className="cell ">
                  <div className="cell-Title">
                    <h2 >GPU Temperature (C°)</h2>
                  </div>
                  <div className="cell-body">
                    {execTimeArray && gpu_TempArray && execTimeArray.length > 0 && gpu_TempArray.length > 0 ? (
                        <div>
                          <MyChart ref={tempChartRef} label={['Temperature','Temperature (°C)']} execution_time={execTimeArray} temperatureArray={gpu_TempArray} />
                        </div>
                      ) : (
                        <p>No data available for the chart.</p>
                    )}
                  </div>
                    
                    
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2>GPU Frequency (MHz)</h2>
                  </div>
                  <div  className="cell-body">
                  { gpuFreq !== null  && (
                      <label className="singleData-metric">{gpuFreq/1000000}</label>
                  )}
                  </div>
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2 >Power Consumption (W)</h2>
                  </div>
                  <div className="cell-body">
                    {execTimeArray && gpu_PowerArray && execTimeArray.length > 0 && gpu_PowerArray.length > 0 ? (
                        <div>
                          <MyChart ref={powerChartRef} label={['Power','Power (W)']} execution_time={execTimeArray} powerArray={gpu_PowerArray} />
                        </div>
                      ) : (
                        <p>No data available for the chart.</p>
                    )}
                  </div>
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2 >RAM In Use</h2>
                  </div>
                  <div className="cell-body">
                    {execTimeArray && gpu_ramArray && execTimeArray.length > 0 && gpu_ramArray.length > 0 ? (
                        <div>
                          <MyChart ref={ramChartRef} label={['RAM','RAM (MB)']} execution_time={execTimeArray} ramArray={gpu_ramArray} />
                        </div>
                      ) : (
                        <p>No data available for the chart.</p>
                    )}
                  </div>
                </div>

                <div className="cell-Metrics">
                  <div className="cell-Title-Metrics">
                    <h2 >General Metrics</h2>
                  </div>
                  <div className="cell-generalMetrics">

                    <div className="execution-info">
                      <p>Type of executions: {props.execType}</p>
                      <p>Number of executions: {props.execNum}</p>
                      <h4> Execution time metrics</h4>
                    </div>

                    <div className="execution-times">
                      <div className="column">
                        {iterationsTime.slice(0, Math.ceil(iterationsTime.length / 2)).map((time, index) => (
                          <p key={`time-${index}`}>{index + 1}) {time + ' s'}</p>
                        ))}
                      </div>
                      <div className="column">
                        {iterationsTime.slice(Math.ceil(iterationsTime.length / 2)).map((time, index) => (
                          <p key={`time-${index + Math.ceil(iterationsTime.length / 2)}`}>{index + Math.ceil(iterationsTime.length / 2) + 1}) {time + ' s'}</p>
                        ))}
                      </div>
                    </div>

                  </div>
                </div>
            </div>
        </div>

    );
}


export default MonitoringView;