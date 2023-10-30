import { useState } from "react";
import './MonitoringView.css';

function MonitoringView (props) {

    const [error, setError] = useState('');
    const [currentApps, setCurrentApps] = useState([]);

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

    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await fetch(props.currentAppsURL);
            const result = await response.json();
            setCurrentApps(result);
          } catch (error) {
            console.error('Error fetching data:', error);
          }
        };
    
        // Call fetchData initially
        fetchData();
    
        // Set up a polling interval (every 1 seconds in this example)
        const intervalId = setInterval(fetchData, 1000);
    
        // Clean up the interval on component unmount
        return () => clearInterval(intervalId);
    }, []);


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
                    {currentApps.map((item) => (
                        <label key={item.id}>{item.name}</label>
                    ))}
                </div>
                
                <div className="cell ">
                    
                </div>
                
                <div className="cell">
                    
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