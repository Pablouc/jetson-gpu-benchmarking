import MainView from "./components/MainView/MainView";

const ngrokURL = 'https://2377-141-3-72-67.ngrok-free.app/';

const gauss_workloadsNamesURL = ngrokURL + 'gauss_workloads';
const bfs_workloadsNamesURL = ngrokURL + 'bfs_workloads';
const requestExecutionURL = ngrokURL + 'setExecutionRequest';
const frequenciesOptionsURL = ngrokURL + 'frequencies';
const resultsFileDataURL = ngrokURL + 'get-csv';
const gpuDataURL = ngrokURL + 'gpu_data';
const executionTimeURL = ngrokURL + "exec_time"


function App() {
  return (
    <div>
      <MainView gauss_workloadsURL={gauss_workloadsNamesURL} bfs_workloadsURL={bfs_workloadsNamesURL} 
                executionURL={requestExecutionURL} frequenciesURL={frequenciesOptionsURL} 
                resultsFileURL={resultsFileDataURL} gpu_dataURL={gpuDataURL} 
                execTimeURL={executionTimeURL}/>
    </div>
  );
}

export default App;
