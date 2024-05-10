import { useState, useEffect, useRef } from "react";
import './MonitoringView.css';
import MyChart from "./MyChart";
import ExecutionTime from "./ExecutionTime";
import ConsoleView from "./ConsoleView";
import io from 'socket.io-client';

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
    const [gpuUsageArray, setGpuUsageArray] = useState([]);
    const [consoleLogs, setConsoleLogs] = useState([]);
    const [timeSamples, setTimeSamples] = useState([]);
    const [frequencySamples, setFrequencySamples] = useState([]);
    const [executionStatus, setExecutionStatus] = useState('');

    const tempChartRef = useRef(null);
    const powerChartRef = useRef(null);
    const freqChartRef = useRef(null);
    const usageChartRef = useRef(null);

    const changeCurrentApps = () =>{
      setCurrentApps([]);
    }

    function parseFileContent(content) {
      const lines = content.split('\n');
      const timeIndex = lines.findIndex(line => line.startsWith('Time samples'));
      const frequencyIndex = lines.findIndex(line => line.startsWith('Frequency samples'));
  
      if (timeIndex !== -1 && lines[timeIndex + 1]) {
        // First, filter to take every 10th element
        const rawTimeData = lines[timeIndex + 1].split(',').map(Number).filter((_, index) => (index % 10) === 0);
        // Then, take the last 100 elements of this filtered set, or all if fewer than 100
        const timeData = rawTimeData.length > 100 ? rawTimeData.slice(-100) : rawTimeData;
        setTimeSamples(timeData);
      }
  
      if (frequencyIndex !== -1 && lines[frequencyIndex + 1]) {
         // First, filter to take every 10th element
        const rawFrequencyData = lines[frequencyIndex + 1].split(',').map(Number).filter((_, index) => (index % 10) === 0);
        // Then, take the last 100 elements of this filtered set, or all if fewer than 100
        const frequencyData = rawFrequencyData.length > 100 ? rawFrequencyData.slice(-100) : rawFrequencyData;
        setFrequencySamples(frequencyData);
      }
    }

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
            if(props.getExecState == 'Injection Fault detected'){
              a.download = 'execution_results.zip'; // Or whatever you want the filename to be
            }
            else{a.download = 'execution_results.zip'; }
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
          if(data != 'out of execution'){
            setGpuTemp(data.global_gpu_data.temperature);
            setGpuFreq(data.global_gpu_data.frequency);
            setPower(data.global_gpu_data.power);
            setGpuTempArray(data.gpu_iterations_data.temperature.map((temp) => parseFloat(temp)));
            setGpuPowerArray(data.gpu_iterations_data.power.map((temp) => parseFloat(temp)));
            setExecTimeArray(data.gpu_iterations_data.current_time);
            setIterationsTime(data.gpu_iterations_data.iteration_time);
            setGpuRamArray(data.gpu_iterations_data.ram_used);
            setGpuUsageArray(data.gpu_iterations_data.gpu_usage);
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
        if (executionStatus === 'InProgress') {
          fetch_GPUData();
      
          // Set up a polling interval (every second in this example) for both
          const pollingIntervalId = setInterval(() => {
            fetch_GPUData();
          }, 1000);
      
            return () => clearInterval(pollingIntervalId);
        }
    }, [props.currentAppsURL, executionStatus, props.gpuData]); 

  
    useEffect(() => {
      setExecutionStatus(props.getExecState)
    }, [props.getExecState]);


    

    useEffect(() => {
      const socket = io(props.ngrokURL, {
        path: '/socket.io/', // Default path for Socket.IO
        transports: ['websocket'] // Force WebSocket transport
      });

      socket.on('connect', () => {
        console.log('Connected to WebSocket server');
        socket.emit('message', 'Hello from React');
      });

      socket.on('connect_error', (error) => {
        console.error('Connection Error:', error);
      });

      socket.on('response', (data) => {
        console.log('Received response:', data);
        // Update the consoleLogs state with the received logs
        if (data.console_logs) {
          if (data.console_logs) {
            const newConsoleLogs = data.console_logs.flatMap(log => log.split('\n'));
            setConsoleLogs(prevLogs => [...prevLogs, ...newConsoleLogs]);
          }
        }
      });

      socket.on('file_transfer', (data) => {
        
        if (data.file_content) {
          parseFileContent(data.file_content);
        }
      });

      socket.on('task_complete', (data) => {
        
        if (data.result) {
          if(data.result.message == 'Execution request processed successfully.'){
            setExecutionStatus('Succeded');
          }
          else if(data.result.message == 'Execution stoped due to injection fault'){
            setExecutionStatus('Injection Fault detected');
          }else{
            setExecutionStatus('Failed');
          }
          
        }
      });

      return () => {
        socket.disconnect();
      };
    }, [props.ngrokURL]);




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
              <div className="labels-container">
                <label className="execution-state">Execution State: {'  '} {executionStatus}</label>
                {/* <label className="execution-time">Execution time: {timer/1000} s</label> */}
                
              </div>

          
            </div>
            <div className="container"> 

                <div className="cell"> 
                  <div className="cell-Title">
                    <h2 >Apps being executed </h2>
                  </div>
                  <div className="cell-body">
                    {executionStatus === "InProgress" ? (
                      currentApps === null ? (
                        <p>Loading...</p>
                      ) : Array.isArray(currentApps) ? (
                        currentApps.map((item, index) => (
                          <div key={index} className="boldText">
                            <div>{item}</div>
                          </div>
                        ))
                      ) : (
                        <p>currentApps is not an array</p>
                      )
                    ) : (
                      <p>Execution is not in progress</p>
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
                      <p>GPU frequency: {gpuFreq}</p>
                      <h4> Execution time metrics</h4>
                    </div>

                    <div className="execution-times">
                      <div className="column">
                        {iterationsTime.slice(0, Math.ceil(iterationsTime.length / 2)).map((time, index) => (
                          <p key={`time-${index}`}>{index + 1}) {parseFloat(time.toFixed(4)) + ' s'}</p>
                        ))}
                      </div>
                      <div className="column">
                        {iterationsTime.slice(Math.ceil(iterationsTime.length / 2)).map((time, index) => (
                          <p key={`time-${index + Math.ceil(iterationsTime.length / 2)}`}>{index + Math.ceil(iterationsTime.length / 2) + 1}) {parseFloat(time.toFixed(4)) + ' s'}</p>
                        ))}
                      </div>
                    </div>

                  </div>
                </div>
                
                <div className="cell ">
                  <div className="cell-Title">
                    <h2 >GPU Temperature (C°)</h2>
                  </div>
                  <div className="cell-body">
                    {execTimeArray && gpu_TempArray && execTimeArray.length > 0 && gpu_TempArray.length > 0 ? (
                        <div>
                          <MyChart ref={tempChartRef} label={['Temperature','Temperature (°C)']} execution_time={execTimeArray.slice(-100)} temperatureArray={gpu_TempArray.slice(-100)} />
                        </div>
                      ) : (
                        <p>No data available for the chart.</p>
                    )}
                  </div>
                    
                    
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2>GPU Usage (%)</h2>
                  </div>
                  <div className="cell-body">
                    {execTimeArray && gpuUsageArray && execTimeArray.length > 0 && gpuUsageArray.length > 0 ? (
                        <div>
                          <MyChart ref={usageChartRef} label={['Usage','Usage (%)']} execution_time={execTimeArray.slice(-100)} usageArray={gpuUsageArray.slice(-100)} />
                        </div>
                      ) : (
                        <p>No data available for the chart.</p>
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
                          <MyChart ref={powerChartRef} label={['Power','Power (W)']} execution_time={execTimeArray.slice(-100)} powerArray={gpu_PowerArray.slice(-100)} />
                        </div>
                      ) : (
                        <p>No data available for the chart.</p>
                    )}
                  </div>
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2 >GPU FREQUENCY (MHz)</h2>
                  </div>
                  <div className="cell-body">
                    {timeSamples && frequencySamples && timeSamples.length > 0 && frequencySamples.length > 0 ? ( 
                        <div>
                          <MyChart ref={freqChartRef} label={['GPU FREQ','FREQ (MHz)']} execution_time={timeSamples} ramArray={frequencySamples} />
                        </div>
                      ) : (
                        <p>No data available for the chart.</p>
                    )}
                  </div>
                </div>


            </div>

            <div>
              <ConsoleView consoleLogs={consoleLogs}> </ConsoleView>
            </div>
        </div>  

    );
}


export default MonitoringView;