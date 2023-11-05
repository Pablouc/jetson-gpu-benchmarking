import { useState, useEffect } from "react";
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
    const [timer, setTimer] = useState(0);
    const [execTimeArray, setExecTimeArray] = useState([]);

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

    const fetch_AppsInUse = () => {
        setError(null);
        fetch(props.currentAppsURL, {
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
            //console.log(data);
            setCurrentApps(data);
          })
          .catch((error) => {
            setError(error.message);
          });
      };

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
            //console.log(data);
            setGpuTemp(data.temperature);
            setGpuFreq(data.frequency);
            setPower(data.power);
          })
          .catch((error) => {
            setError(error.message);
          });
      };


      const fetch_GPUIterationsData = () => {
        setError(null);
        fetch(props.gpu_IterDataURL, {
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
            //console.log(data);
            setGpuTempArray(data.temperature);
            setGpuPowerArray(data.power);
            setExecTimeArray(data.exec_time);
          })
          .catch((error) => {
            setError(error.message);
          });
      };

    useEffect(() => {
        if (props.getExecState === 'InProgress') {
          fetch_AppsInUse();
          fetch_GPUData();
          fetch_GPUIterationsData();
      
          // Set up a polling interval (every second in this example) for both
          const pollingIntervalId = setInterval(() => {
            fetch_AppsInUse();
            fetch_GPUData();
            fetch_GPUIterationsData();
          }, 1000);
      
            return () => clearInterval(pollingIntervalId);
        }
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
                      ) : (
                          currentApps.map((item, index) => (
                              <div key={index} className="boldText">{item}</div>
                          ))
                      )}

                  </div>
                </div>
                
                <div className="cell ">
                  <div className="cell-Title">
                    <h2 className="cell-Title">GPU Temperature (C°)</h2>
                  </div>
                  <div className="cell-body">
                  { gpuTemp !== null  && (
                      <label className="singleData-metric">{gpuTemp}</label>
                  )}
                  </div>
                    
                    
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2>GPU Frequency (MHz)</h2>
                  </div>
                  <div  className="cell-body">
                  { gpuFreq !== null  && (
                      <label className="singleData-metric">{gpuFreq}</label>
                  )}
                  </div>
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2 >Power Consumption (W)</h2>
                  </div>
                  <div className="cell-body">
                    { gpuPower !== null  && (
                        <label className="singleData-metric">{gpuPower}</label>
                    )}
                  </div>
                </div>
                
                <div className="cell">
                  <div className="cell-Title">
                    <h2 >Threads In Use</h2>
                  </div>
                  <div className="cell-body"></div>
                </div>

                <div className="cell">
                  <div className="cell-Title">
                    <h2 >Power Vs Temperature</h2>
                  </div>
                  <div className="cell-body">
                    <MyChart execution_time={execTimeArray} temperatureArray={gpu_TempArray}/>
                  </div>
                </div>
            </div>
        </div>

    );
}


export default MonitoringView;