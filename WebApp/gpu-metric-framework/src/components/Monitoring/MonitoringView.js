import { useState, useEffect } from "react";
import './MonitoringView.css';

function MonitoringView (props) {

    const [error, setError] = useState('');
    const [currentApps, setCurrentApps] = useState([]);
    const [gpuTemp, setGpuTemp] =  useState('');
    const [gpuFreq, setGpuFreq] =  useState('');

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
        console.log(props.gpu_dataURL);
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
            //setGpuTemp(data.temperature);
            //setGpuFreq(data.frequency);
          })
          .catch((error) => {
            setError(error.message);
          });
      };

    useEffect(() => {
        if (props.getExecState === 'InProgress') {
          console.log('before AppsInUse')
          fetch_AppsInUse();
          console.log('afer AppsInUse')
           fetch_GPUData();
           console.log('before GPUData')
      
            // Set up a polling interval (every 5 seconds in this example) for both
            const pollingIntervalId = setInterval(() => {
              fetch_AppsInUse();
              fetch_GPUData();
            }, 1000);
      
            return () => clearInterval(pollingIntervalId);
        }
    }, [props.currentAppsURL, currentApps, props.getExecState, props.gpuData]);


    const changeView=()=>{
        props.setView(false);
    }


    return(
        <div>
        
            <div>
                <button className="monitoring-button" onClick={downloadResults}>Download results</button>
                <button className="monitoring-button" onClick={changeView}>Request Execution</button>
            </div>
            <div className="container">
                <div className="cell"> 
                    <h4 className="cell-Title">Apps being executed </h4>
                    {currentApps === null ? (
                        <p>Loading...</p>
                    ) : (
                        currentApps.map((item, index) => (
                            <div key={index} className="boldText">{item}</div>
                        ))
                    )}
                </div>
                
                <div className="cell ">
                    GPU Temperature: {gpuTemp !== null ? gpuTemp : "Loading..."}
                </div>
                
                <div className="cell">
                    GPU Frequency: {gpuFreq !== null ? gpuFreq : "Loading..."}
                </div>
                
                <div className="cell">
                    
                </div>
                
                <div className="cell">
                    
                </div>

                <div className="cell">
                    
                </div>
            </div>
        </div>

    );
}


export default MonitoringView;